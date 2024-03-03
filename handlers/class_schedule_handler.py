from contextlib import suppress
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from database import User, Class
from keyboards import fabrics

router = Router()

START_DATE: datetime = datetime(2023, 9, 4)
MAX_DAY: int = 5
MIN_DAY: int = 0
MAX_WEEK: int = 41
MIN_WEEK: int = 1


@router.message(F.text == "🗓️ Class schedule")
@router.message(Command("classes"))
async def class_schedule_command(message: Message, session: AsyncSession):
    current_date, day_num = get_nearest_date(datetime.now())

    week_num = get_relative_week_num(START_DATE, current_date)

    user = await session.execute(select(User).where(User.user_id == message.from_user.id))
    user = user.scalar()
    day_schedule: str = await get_formatted_day_schedule(current_date, user.study_group, session)

    await message.answer(
        day_schedule,
        reply_markup=fabrics.get_double_paginator(
            day_num, week_num, current_date.strftime("%A"), f"{week_num}/{MAX_WEEK}"
        )
    )


@router.callback_query(fabrics.DoublePagination.filter(
    F.action.in_(["prev_page", "next_page", "prev_section", "next_section"])))
async def class_schedule_pagination_callback(call: CallbackQuery, callback_data: fabrics.DoublePagination,
                                             session: AsyncSession):
    current_day: int = callback_data.page
    current_week: int = callback_data.section

    new_week: int = current_week

    def update_value(current_value: int, min_value: int, max_value: int, decrement: bool = False):
        delta = -1 if decrement else 1
        return (current_value + delta - min_value) % (max_value - min_value + 1) + min_value

    if callback_data.action in ["next_section", "prev_section"]:
        new_week = update_value(current_week, MIN_WEEK, MAX_WEEK, decrement=(callback_data.action == "prev_section"))
        new_day = MIN_DAY
    else:
        new_day = update_value(current_day, MIN_DAY, MAX_DAY, decrement=(callback_data.action == "prev_page"))
        if callback_data.action == "next_page" and new_day == MIN_DAY:
            new_week = update_value(current_week, MIN_WEEK, MAX_WEEK)
        elif callback_data.action == "prev_page" and new_day == MAX_DAY:
            new_week = update_value(current_week, MIN_WEEK, MAX_WEEK, decrement=True)

    new_date = START_DATE + timedelta(days=new_day, weeks=new_week-1)

    user = await session.execute(select(User).where(User.user_id == call.from_user.id))
    user = user.scalar()
    message = await get_formatted_day_schedule(new_date, user.study_group, session)

    with suppress(TelegramBadRequest):
        weeks_count: str = f"{new_week}/{MAX_WEEK}"

        await call.message.edit_text(
            message,
            reply_markup=fabrics.get_double_paginator(new_day, new_week, new_date.strftime("%A"), weeks_count)
        )
        await call.answer()


async def get_formatted_day_schedule(date_time: datetime, study_group: str, session: AsyncSession):
    sql_query = select(
        Class.start_time,
        Class.subject_name,
        Class.room,
        Class.teacher,
        Class.subgroup
        ).where(
        (Class.start_time.date() >= date_time.date()) &
        (Class.start_time.date() < date_time.date() + timedelta(days=1)) &
        (Class.study_group == study_group)
    )
    result = await session.execute(sql_query)

    classes = result.all()

    message = (
        f"🗓️ <b>WEEK {get_relative_week_num(START_DATE, date_time)} | " 
        f"{date_time.strftime('%A')} ({date_time.strftime('%d.%m.%Y')})</b>\n\n"
        )

    time_format: str = "%H:%M"

    for class_data in classes:
        time_range: str = "{} - {}".format(
            class_data.start_time.strftime(time_format),
            (class_data.start_time + timedelta(minutes=85)).strftime(time_format)
        )

        class_message = "\n".join((
            f"<b>{class_data.subject_name}</b>",
            f"| 🕓 <code>{time_range}</code>\n",
        ))

        if class_data.room:
            class_message += f"| 📍 <code>{class_data.room}</code>\n"
        if class_data.teacher:
            class_message += f"| 👨‍🏫 <code>{class_data.teacher}</code>\n"
        if class_data.subgroup:
            class_message += f"| 🔗 <code>{class_data.subgroup}</code>\n"

        message += (class_message + "\n")
    return message


def get_relative_week_num(start_datetime: datetime, current_datetime: datetime) -> int:
    if start_datetime > current_datetime:
        raise ValueError("start_datetime must be earlier than current_datetime")
    return (current_datetime - start_datetime).days // 7 + 1


def get_nearest_date(current_date: datetime):
    day_num = current_date.weekday()

    if day_num > MAX_DAY:
        current_date += timedelta(days=7 - day_num)
        day_num = MIN_DAY

    return current_date, day_num
