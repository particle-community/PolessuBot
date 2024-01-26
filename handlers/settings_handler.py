from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import STUDY_GROUPS
from database import User
from keyboards import inline, fabrics

router = Router()

SETTINGS_MESSAGE: str = (
    "⚙️ <b>Settings</b>\n\n"
    "㊗️ Language: <code>{0}</code>\n"
    "🎓 Study group: <code>{1}</code>"
)
IN_DEVELOPMENT_MESSAGE: str = (
    "⚠️ <b>Function in development</b>\n\n"
    "However, our team is actively working on this! 🚀"
)
SWITCH_GROUP_MESSAGE = (
    "🎓 <b>Switch group</b>\n\n"
    "Select one of the available options"
)
SETTINGS_UPDATE_MESSAGE = (
    "🔄 <b>Settings updated</b>\n\n"
    "{0} to <i>{1}</i>"
)


@router.message(F.text == "⚙️ Settings")
@router.message(Command("settings"))
async def settings_command(message: Message, session: AsyncSession):
    user = await session.execute(select(User).where(User.user_id == message.from_user.id))
    user = user.scalar()

    await message.answer(
        SETTINGS_MESSAGE.format("🇬🇧 English", user.study_group),
        reply_markup=inline.settings_menu
    )


@router.callback_query(F.data == "to_settings")
async def settings_callback(call: CallbackQuery, session: AsyncSession):
    user = await session.execute(select(User).where(User.user_id == call.from_user.id))
    user = user.scalar()

    await call.message.edit_text(
        SETTINGS_MESSAGE.format("🇬🇧 English", user.study_group),
        reply_markup=inline.settings_menu
    )
    await call.answer()


@router.callback_query(F.data == "change_language")
async def change_language_callback(call: CallbackQuery):
    await call.message.edit_text(
        IN_DEVELOPMENT_MESSAGE,
        reply_markup=inline.settings_back
    )
    await call.answer()


@router.callback_query(F.data == "switch_group")
async def switch_group_callback(call: CallbackQuery):
    await call.message.edit_text(
        SWITCH_GROUP_MESSAGE,
        reply_markup=fabrics.get_switch_group_keyboard(STUDY_GROUPS)
    )
    await call.answer()


@router.callback_query(fabrics.SettingsAction.filter(F.action == "update_group"))
async def update_study_group_callback(call: CallbackQuery, callback_data: fabrics.SettingsAction, session: AsyncSession):
    user = await session.execute(select(User).where(User.user_id == call.from_user.id))
    user = user.scalar()

    new_group = callback_data.value

    user.study_group = new_group
    await session.commit()

    await call.message.edit_text(
        SETTINGS_UPDATE_MESSAGE.format("The group switched", new_group),
        reply_markup=inline.settings_back
    )
    await call.answer("🔄 Study group switched")
