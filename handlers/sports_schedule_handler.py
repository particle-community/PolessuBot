from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

router = Router()

SPORTS_SCHEDULE_MESSAGE: str = (
    "⚒ <b>Function in development</b> 🚧\n\n"
    "...but we are already working on it! 🚀"
)


@router.message(F.text == "⚽ Sports schedule")
@router.message(Command(commands=["sports_schedule", "sports"]))
async def sports_schedule_command(message: Message):
    await message.answer(
        SPORTS_SCHEDULE_MESSAGE
    )


@router.callback_query(F.data == "sports_schedule")
async def sports_schedule_callback(call: CallbackQuery):
    await call.message.answer(
        SPORTS_SCHEDULE_MESSAGE
    )
    await call.answer()
