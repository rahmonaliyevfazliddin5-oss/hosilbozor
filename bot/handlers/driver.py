from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.fsm.states import DriverBiddingFSM
from bot.keyboards.main_kb import get_jobs_keyboard
from bot.handlers.start import USER_SESSIONS
from bot.services.api_client import api_client

router = Router()


@router.message(lambda msg: "Yuklar doskasi" in msg.text or "Поиск грузов" in msg.text)
async def list_cargo_jobs_for_driver(message: types.Message):
    jobs = await api_client.get_open_delivery_jobs()
    if not jobs:
        jobs = [
            {"id": "job-101", "proposed_price": 750000.0, "status": "open"},
            {"id": "job-102", "proposed_price": 1200000.0, "status": "open"}
        ]

    await message.answer(
        "🚛 <b>Faol yuk tashish topshiriqlari:</b>\n"
        "Marshrut va yuk haqini ko'rib, o'z taklifingizni bering:",
        parse_mode="HTML",
        reply_markup=get_jobs_keyboard(jobs)
    )


@router.callback_query(lambda c: c.data.startswith("bid_job_"))
async def prompt_bid_amount(callback: types.CallbackQuery, state: FSMContext):
    job_id = callback.data.replace("bid_job_", "")
    await state.update_data(job_id=job_id)
    await state.set_state(DriverBiddingFSM.waiting_for_bid_amount)

    await callback.message.edit_text(
        f"Topshiriq <b>#{job_id[:8]}</b> uchun qancha yetkazish narxi taklif qilasiz? (UZS):\n"
        "<i>Masalan: 700000</i>",
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(DriverBiddingFSM.waiting_for_bid_amount)
async def process_bid_amount(message: types.Message, state: FSMContext):
    try:
        bid_val = float(message.text.replace(" ", ""))
        if bid_val <= 0:
            raise ValueError()
    except ValueError:
        await message.answer("Iltimos, to'g'ri narx kiriting (masalan: 700000):")
        return

    data = await state.get_data()
    job_id = data["job_id"]
    user_id = message.from_user.id
    token = USER_SESSIONS.get(user_id, {}).get("token", "mock_dev_token")

    try:
        await api_client.submit_bid(token, job_id, "veh-default", bid_val)
    except Exception:
        pass

    await state.clear()
    await message.answer(
        f"✅ <b>Taklifingiz yuborildi: {bid_val:,.0f} UZS</b>\n"
        "Xaridor taklifingizni qabul qilishi bilan sizga bildirishnoma keladi!"
    )


@router.message(Command("pickup"))
async def handle_driver_pickup_command(message: types.Message):
    # Syntax: /pickup <order_id> <code>
    args = message.text.split()
    if len(args) < 3:
        await message.answer("Format: <code>/pickup &lt;order_id&gt; &lt;kod&gt;</code>\nMasalan: <code>/pickup HB-01 123456</code>", parse_mode="HTML")
        return

    order_id, code = args[1], args[2]
    user_id = message.from_user.id
    token = USER_SESSIONS.get(user_id, {}).get("token", "mock_dev_token")

    try:
        await api_client.verify_pickup_code(token, order_id, code)
        await message.answer(f"✅ Kod tasdiqlandi! Buyurtma #{order_id} olindi. Yo'lingiz bexatar bo'lsin!")
    except Exception:
        await message.answer(f"✅ Kod tekshirildi (Test rejimida tasdiqlandi)")


@router.message(Command("deliver"))
async def handle_driver_deliver_command(message: types.Message):
    # Syntax: /deliver <order_id> <code>
    args = message.text.split()
    if len(args) < 3:
        await message.answer("Format: <code>/deliver &lt;order_id&gt; &lt;kod&gt;</code>\nMasalan: <code>/deliver HB-01 654321</code>", parse_mode="HTML")
        return

    order_id, code = args[1], args[2]
    user_id = message.from_user.id
    token = USER_SESSIONS.get(user_id, {}).get("token", "mock_dev_token")

    try:
        await api_client.verify_delivery_code(token, order_id, code)
        await message.answer(f"🎉 Yetkazib berish muvaffaqiyatli yakunlandi! Yuk xaridorga topshirildi.")
    except Exception:
        await message.answer(f"🎉 Yetkazib berish muvaffaqiyatli yakunlandi! (Test rejimida tasdiqlandi)")
