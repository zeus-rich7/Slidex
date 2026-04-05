import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

from src import middlewares, handlers
from config import load_config
from src.handlers.user.presentation_menu import routes
from src.helpers import Config
from src.infrastructure.database import create_pool, make_connection_string

dp = Dispatcher()


async def on_startup():
    await Config().initialize()
    await Config.refresh()



async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    bot = Bot(token=config.tgbot.token, default=DefaultBotProperties(parse_mode="HTML"))

    def create_app() -> web.Application:
        app = web.Application()
        app.add_routes(routes)

        # Share bot & dp with handlers if needed
        app["bot"] = bot
        app["dp"] = dp

        return app

    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)  # or 443 with SSL
    await site.start()

    pool = create_pool(url=make_connection_string(config))
    middlewares.setup(dp, pool=pool)
    handlers.setup(dp)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
