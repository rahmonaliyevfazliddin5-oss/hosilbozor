from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from bot.keyboards.main_kb import get_main_menu_keyboard, get_language_selection_keyboard
from bot.services.api_client import api_client

router = Router()

# In-memory session store: tg_id -> {"token": "...", "lang": "uz_latn"}
USER_SESSIONS = {}


@router.message(CommandStart())
async def handle_start(message: types.Message):
    tg_user = message.from_user
    lang = "uz_latn"

    try:
        auth_data = await api_client.telegram_login(
            telegram_id=tg_user.id,
            first_name=tg_user.first_name,
            username=tg_user.username,
            role="farmer"
        )
        USER_SESSIONS[tg_user.id] = {
            "token": auth_data.get("access_token"),
            "lang": lang
        }
    except Exception:
        # Fallback for offline dev
        USER_SESSIONS[tg_user.id] = {"token": "mock_dev_token", "lang": lang}

    welcome_text = (
        f"Assalomu alaykum, <b>{tg_user.first_name}</b>!\n\n"
        "🌾 <b>HosilBozor</b> platformasiga xush kelibsiz!\n\n"
        "Bu yerda siz:\n"
        "• Hosilingizni <b>60 soniyada</b> vositachilarsiz sotasiz\n"
        "• Viloyat bozorlaridagi <b>eng so'nggi ulgurji narxlarni</b> ko'rasiz\n"
        "• Yuk mashinalarini to'g'ridan-to'g'ri topasiz\n"
        "• Xavfsiz <b>Escrow to'lovi</b> orqali mablag'ingizni kafolatlaysiz.\n\n"
        "Quyidagi menyudan kerakli bo'limni tanlang:"
    )

    await message.answer(
        welcome_text,
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard(lang)
    )


@router.message(lambda msg: "Tilni o'zgartirish" in msg.text or "Изменить язык" in msg.text)
async def handle_language_prompt(message: types.Message):
    await message.answer(
        "Iltimos, o'zingizga qulay tilni tanlang:\nВыберите удобный язык:",
        reply_markup=get_language_selection_keyboard()
    )


@router.callback_query(lambda c: c.data.startswith("set_lang_"))
async def handle_set_language(callback: types.CallbackQuery):
    lang_code = callback.data.replace("set_lang_", "")
    user_id = callback.from_user.id
    if user_id in USER_SESSIONS:
        USER_SESSIONS[user_id]["lang"] = lang_code

    confirmation = "Til o'zgartirildi: O'zbekcha ✅" if "uz" in lang_code else "Язык успешно изменен: Русский ✅"
    await callback.message.edit_text(confirmation)
    await callback.message.answer(
        "Bosh menyu:",
        reply_markup=get_main_menu_keyboard(lang_code)
    )
    await callback.answer()
