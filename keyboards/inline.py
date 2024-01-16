from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

settings_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="㊗️ Change language", callback_data="change_language")
        ],
        [
            InlineKeyboardButton(text="🎓 Switch group", callback_data="switch_group")
        ]
    ]
)

settings_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Back", callback_data="to_settings")
        ]
    ]
)
