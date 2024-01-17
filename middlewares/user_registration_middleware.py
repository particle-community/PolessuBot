from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from sqlalchemy import select

from config import STUDY_GROUPS
from database import User


class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        session = data.get("session")
        user_data = event.from_user

        if session:
            user_id = user_data.id
            user = await session.execute(select(User).where(User.user_id == user_id))
            user = user.scalar()

            if not user:
                session.add(User(
                    user_id=user_id,
                    username=user_data.username,
                    study_group=STUDY_GROUPS[0],
                    language_code=user_data.language_code
                ))
                await session.commit()

        return await handler(event, data)
