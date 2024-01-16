from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗓️ Class schedule")
        ],
        [
            KeyboardButton(text="⚽ Sports schedule")
        ],
        [
            KeyboardButton(text="⚙️ Settings"),
        ]
    ],
    resize_keyboard=True
)
