from aiogram import Router
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.video.downloader import download_telegram_video

router = Router()


@router.message(lambda message: message.video is not None)
async def video_handler(message: Message):

    duration = message.video.duration

    if duration > 1200:
        return await message.answer(
            "❌ Maximum allowed video length is 20 minutes."
        )

    status = await message.answer(
        "📥 Downloading video..."
    )

    filepath = await download_telegram_video(
        message.bot,
        message.video
    )

    kb = InlineKeyboardBuilder()

    kb.button(text="10s", callback_data="duration_10")
    kb.button(text="15s", callback_data="duration_15")
    kb.button(text="30s", callback_data="duration_30")
    kb.button(text="60s", callback_data="duration_60")

    kb.adjust(2)

    await status.edit_text(
        f"✅ Video Saved\n\n"
        f"📁 {filepath}\n\n"
        f"🎬 Select Clip Duration",
        reply_markup=kb.as_markup()
    )


@router.message()
async def youtube_handler(message: Message):

    text = message.text or ""

    if "youtube.com" in text or "youtu.be" in text:

        kb = InlineKeyboardBuilder()

        kb.button(text="10s", callback_data="duration_10")
        kb.button(text="15s", callback_data="duration_15")
        kb.button(text="30s", callback_data="duration_30")
        kb.button(text="60s", callback_data="duration_60")

        kb.adjust(2)

        await message.answer(
            "🔗 YouTube Link Received\n\n"
            "🎬 Select Clip Duration",
            reply_markup=kb.as_markup()
        )
