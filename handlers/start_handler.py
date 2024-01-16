from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import reply

router = Router()

START_MESSAGE: str = (
        "<b>Welcome to <a href=\"https://t.me/polessu_schedule_bot\">PolesSU Bot</a> 👋</b>\n\n"
        "Here you can get the current schedule of classes and sports facilities of PolesSU\n\n"
        "Join us: <a href=\"https://t.me/+tZ1rie_oLXljMjJi\">🔗 Particle Community</a>"
)


@router.message(Command(commands=["start", "menu"]))
async def start_command(message: Message):
    await message.answer(
        START_MESSAGE,
        reply_markup=reply.main_menu
    )
