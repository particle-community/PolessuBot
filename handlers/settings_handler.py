from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import User
from keyboards import inline

router = Router()

SETTINGS_MESSAGE: str = (
    "⚙️ <b>Settings</b>\n\n"
    "㊗️ Language: <i>{0}</i>\n"
    "🎓 Study group: <i>{1}</i>"
)
IN_DEVELOPMENT_MESSAGE: str = (
    "⚒ <b>Function in development</b> 🚧\n\n"
    "...but we are already working on it! 🚀"
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
        IN_DEVELOPMENT_MESSAGE,
        reply_markup=inline.settings_back
    )
    await call.answer()
