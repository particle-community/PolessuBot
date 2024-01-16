import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import (
    BOT_TOKEN,
    WEBHOOK_TOKEN,
    WEBHOOK_HOST,
    WEBHOOK_PATH,
    WEB_SERVER_HOST,
    WEB_SERVER_PORT,
    sessionmaker,
)
from handlers import *
from middlewares import DatabaseSessionMiddleware, UserRegistrationMiddleware


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{WEBHOOK_HOST}{WEBHOOK_PATH}", secret_token=WEBHOOK_TOKEN, drop_pending_updates=True)


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()


def main() -> None:
    dp = Dispatcher()

    dp.update.middleware(DatabaseSessionMiddleware(session_pool=sessionmaker))
    dp.message.middleware(UserRegistrationMiddleware())

    dp.include_routers(
        class_schedule_handler.router,
        settings_handler.router,
        sports_schedule_handler.router,
        start_handler.router
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_TOKEN,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
