from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from config import STUDY_GROUPS


class SinglePagination(CallbackData, prefix="spg"):
    action: str
    page: int


class DoublePagination(CallbackData, prefix="dpg"):
    action: str
    page: int
    section: int


class SettingsAction(CallbackData, prefix="sac"):
    action: str
    value: str


def get_single_paginator(page: int = 1, value: str = None) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="◀️", callback_data=SinglePagination(action="prev", page=page).pack()),
        InlineKeyboardButton(text="▶️", callback_data=SinglePagination(action="next", page=page).pack())
    ]

    if value:
        buttons.insert(1, InlineKeyboardButton(
            text=value,
            callback_data=SinglePagination(action="value", page=page).pack()
        ))

    builder = InlineKeyboardBuilder()
    builder.row(*buttons)
    return builder.as_markup()


def get_double_paginator(page: int = 1, section: int = 1,
                         page_value: str = None, section_value: str = None) -> InlineKeyboardMarkup:
    page_buttons = [
        InlineKeyboardButton(
            text="◀️",
            callback_data=DoublePagination(action="prev_page", page=page, section=section).pack()
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=DoublePagination(action="next_page", page=page, section=section).pack()
        )
    ]
    section_buttons = [
        InlineKeyboardButton(
            text="⏪",
            callback_data=DoublePagination(action="prev_section", page=page, section=section).pack()
        ),
        InlineKeyboardButton(
            text="⏩",
            callback_data=DoublePagination(action="next_section", page=page, section=section).pack()
        )
    ]

    if page_value:
        page_buttons.insert(1, InlineKeyboardButton(
            text=page_value,
            callback_data=DoublePagination(action="page_value", page=page, section=section).pack()
        ))

    if section_value:
        section_buttons.insert(1, InlineKeyboardButton(
            text=section_value,
            callback_data=DoublePagination(action="section_value", page=page, section=section).pack()
        ))

    builder = InlineKeyboardBuilder()
    builder.row(*page_buttons)
    builder.row(*section_buttons)
    return builder.as_markup()


def get_switch_group_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for group_name in STUDY_GROUPS:
        builder.row(InlineKeyboardButton(
            text=group_name,
            callback_data=SettingsAction(action="switch_group", value=group_name).pack()
        ))
    return builder.as_markup()
