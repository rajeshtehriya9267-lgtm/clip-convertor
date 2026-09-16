from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.database.users import save_user

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):

    await save_user(message.from_user)

    text = """
🎬 <b>Clip Convertor</b>

Send a video or YouTube link.

✨ Features:
• Highlight Detection
• Custom Clip Duration
• Multiple Clips
• Direct Telegram Delivery
"""

    await message.answer(text)
