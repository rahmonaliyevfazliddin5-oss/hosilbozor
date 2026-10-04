from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)
from typing import List, Dict, Any


def get_main_menu_keyboard(lang: str = "uz_latn") -> ReplyKeyboardMarkup:
    # Text localized for Uzbek (default) and Russian
    btn_harvest = "🌾 Hosil joylash (60 soniya)" if lang == "uz_latn" else "🌾 Добавить урожай (60 сек)"
    btn_prices = "📊 Bozor narxlari" if lang == "uz_latn" else "📊 Цены на базарах"
    btn_cargo = "🚛 Yuklar doskasi" if lang == "uz_latn" else "🚛 Поиск грузов"
    btn_miniapp = "📱 HosilBozor Mini App" if lang == "uz_latn" else "📱 Открыть Mini App"
    btn_lang = "🌐 Tilni o'zgartirish" if lang == "uz_latn" else "🌐 Изменить язык"

    # Mini App URL (e.g. localhost/tma or production hosted url)
    tma_url = "https://hosilbozor.uz/tma"

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=btn_harvest), KeyboardButton(text=btn_prices)],
            [KeyboardButton(text=btn_cargo)],
            [KeyboardButton(text=btn_miniapp, web_app=WebAppInfo(url=tma_url))],
            [KeyboardButton(text=btn_lang)]
        ],
        resize_keyboard=True
    )


def get_crop_selection_keyboard(crops: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    buttons = []
    # 2 buttons per row
    row = []
    for crop in crops:
        row.append(InlineKeyboardButton(text=f"🍅 {crop['name_uz']}", callback_data=f"crop_{crop['id']}_{crop['slug']}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    buttons.append([InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_action")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_confirm_listing_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ E'lonni chiqarish", callback_data="confirm_listing_yes"),
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_action")
            ]
        ]
    )


def get_jobs_keyboard(jobs: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    buttons = []
    for j in jobs[:5]:
        price_str = f"{j['proposed_price']} UZS" if j.get("proposed_price") else "Kelishiladi"
        buttons.append([
            InlineKeyboardButton(
                text=f"📦 Yuk #{j['id'][:6]} — {price_str}",
                callback_data=f"bid_job_{j['id']}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔄 Yangilash", callback_data="refresh_jobs")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_language_selection_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbekcha (Lotin)", callback_data="set_lang_uz_latn"),
                InlineKeyboardButton(text="🇺🇿 Ўзбекча (Кирилл)", callback_data="set_lang_uz_cyrl"),
            ],
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru")
            ]
        ]
    )
