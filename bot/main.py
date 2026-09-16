from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN

from bot.handlers.start import router as start_router
from bot.handlers.video import router as video_router
from bot.handlers.callbacks import router as callback_router

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(video_router)
dp.include_router(callback_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
