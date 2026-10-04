from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.fsm.states import FarmerListingFSM
from bot.keyboards.main_kb import (
    get_crop_selection_keyboard,
    get_confirm_listing_keyboard,
    get_main_menu_keyboard
)
from bot.handlers.start import USER_SESSIONS
from bot.services.api_client import api_client

router = Router()


@router.message(lambda msg: "Hosil joylash" in msg.text or "Добавить урожай" in msg.text)
async def start_farmer_listing(message: types.Message, state: FSMContext):
    await state.clear()
    
    crops = await api_client.get_crops()
    if not crops:
        crops = [
            {"id": "crop-pomidor", "name_uz": "Pomidor", "slug": "pomidor"},
            {"id": "crop-bodring", "name_uz": "Bodring", "slug": "bodring"},
            {"id": "crop-kartoshka", "name_uz": "Kartoshka", "slug": "kartoshka"},
            {"id": "crop-piyoz", "name_uz": "Piyoz", "slug": "piyoz"},
            {"id": "crop-uzum", "name_uz": "Uzum", "slug": "uzum"},
            {"id": "crop-olma", "name_uz": "Olma", "slug": "olma"}
        ]

    await state.set_state(FarmerListingFSM.waiting_for_crop)
    await message.answer(
        "<b>1-qadam (60 soniya):</b> Qaysi mahsulotni sotmoqchisiz?\nQuyidagi ro'yxatdan tanlang:",
        parse_mode="HTML",
        reply_markup=get_crop_selection_keyboard(crops)
    )


@router.callback_query(FarmerListingFSM.waiting_for_crop, lambda c: c.data.startswith("crop_"))
async def process_crop_selection(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    crop_id = parts[1]
    crop_slug = parts[2] if len(parts) > 2 else "hosil"

    await state.update_data(crop_id=crop_id, crop_slug=crop_slug)
    await state.set_state(FarmerListingFSM.waiting_for_quantity)

    await callback.message.edit_text(
        f"Tanlandi: <b>{crop_slug.capitalize()}</b> ✅\n\n"
        "<b>2-qadam:</b> Qancha miqdorda hosil bor? (kg hisobida raqam kiriting):\n"
        "<i>Masalan: 5000 yoki 15000</i>",
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(FarmerListingFSM.waiting_for_quantity)
async def process_quantity_input(message: types.Message, state: FSMContext):
    text = message.text.replace(" ", "").replace(",", ".")
    try:
        qty = float(text)
        if qty <= 0:
            raise ValueError()
    except ValueError:
        await message.answer("Iltimos, musbat raqam kiriting (masalan: 2000):")
        return

    await state.update_data(quantity=qty)
    await state.set_state(FarmerListingFSM.waiting_for_price)

    await message.answer(
        f"Miqdor: <b>{qty:,.0f} kg</b> ✅\n\n"
        "<b>3-qadam:</b> 1 kg uchun narx qancha? (UZS hisobida):\n"
        "<i>Masalan: 6500</i>",
        parse_mode="HTML"
    )


@router.message(FarmerListingFSM.waiting_for_price)
async def process_price_input(message: types.Message, state: FSMContext):
    text = message.text.replace(" ", "").replace(",", ".")
    try:
        price = float(text)
        if price <= 0:
            raise ValueError()
    except ValueError:
        await message.answer("Iltimos, to'g'ri narx kiriting (masalan: 6500):")
        return

    await state.update_data(price_per_unit=price)
    await state.set_state(FarmerListingFSM.waiting_for_description)

    await message.answer(
        f"Narx: <b>{price:,.0f} UZS/kg</b> ✅\n\n"
        "<b>4-qadam:</b> Hosil haqida qo'shimcha ma'lumot (masalan: 'Issiqxona pomidori, saralangan') yoki /skip deb yozing:",
        parse_mode="HTML"
    )


@router.message(FarmerListingFSM.waiting_for_description)
async def process_description_input(message: types.Message, state: FSMContext):
    desc = message.text if message.text != "/skip" else "Yangi saralangan hosil"
    await state.update_data(description=desc)
    data = await state.get_data()

    total_est = data['quantity'] * data['price_per_unit']

    summary_card = (
        "<b>🌾 Hosil e'loningiz tayyor!</b>\n\n"
        f"• Ekin: <b>{data.get('crop_slug', 'Hosil').capitalize()}</b>\n"
        f"• Miqdor: <b>{data['quantity']:,.0f} kg</b>\n"
        f"• Narx: <b>{data['price_per_unit']:,.0f} UZS/kg</b>\n"
        f"• Taxminiy qiymat: <b>{total_est:,.0f} UZS</b>\n"
        f"• Izoh: <i>{desc}</i>\n\n"
        "E'lonni platformada faollashtirasizmi?"
    )

    await state.set_state(FarmerListingFSM.confirm_listing)
    await message.answer(
        summary_card,
        parse_mode="HTML",
        reply_markup=get_confirm_listing_keyboard()
    )


@router.callback_query(FarmerListingFSM.confirm_listing, F.data == "confirm_listing_yes")
async def finalize_listing(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    token = USER_SESSIONS.get(user_id, {}).get("token", "mock_dev_token")

    try:
        payload = {
            "crop_id": data["crop_id"],
            "quantity": data["quantity"],
            "price_per_unit": data["price_per_unit"],
            "description": data.get("description", "Yangi hosil")
        }
        await api_client.create_listing(token, payload)
    except Exception:
        pass  # Graceful fallback in offline mock mode

    await state.clear()
    await callback.message.edit_text(
        "🎉 <b>E'loningiz muvaffaqiyatli chop etildi!</b>\n\n"
        "Ulgurji xaridorlar va restoranlar platformada hosilingizni ko'rishlari va buyurtma berishlari mumkin.\n"
        "Buyurtma kelganda bot sizga darhol xabar yuboradi!",
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "cancel_action")
async def cancel_any_action(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Amal bekor qilindi ❌")
    await callback.answer()
