from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

SPORTS_SCHEDULE_MESSAGE: str = (
    "⚠️ <b>Function in development</b>\n\n"
    "However, our team is actively working on this! 🚀"
)


@router.message(F.text == "⚽ Sports schedule")
@router.message(Command("sports"))
async def sports_schedule_command(message: Message):
    await message.answer(
        SPORTS_SCHEDULE_MESSAGE
    )
