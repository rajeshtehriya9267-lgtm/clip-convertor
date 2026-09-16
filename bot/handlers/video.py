from aiogram import Router
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.video.downloader import download_telegram_video
from bot.video.youtube import download_youtube_video
from bot.handlers.callbacks import video_storage

router = Router()


def duration_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(text="10s", callback_data="duration_10")
    kb.button(text="15s", callback_data="duration_15")
    kb.button(text="30s", callback_data="duration_30")
    kb.button(text="60s", callback_data="duration_60")

    kb.adjust(2)

    return kb.as_markup()


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

    video_storage[
        message.from_user.id
    ] = filepath

    await status.edit_text(
        "✅ Video Received\n\n"
        "🎬 Select Clip Duration",
        reply_markup=duration_keyboard()
    )


@router.message()
async def youtube_handler(message: Message):

    text = message.text or ""

    if "youtube.com" not in text and "youtu.be" not in text:
        return

    status = await message.answer(
        "📥 Downloading YouTube video..."
    )

    try:

        filepath = await download_youtube_video(text)

        video_storage[
            message.from_user.id
        ] = filepath

        await status.edit_text(
            "✅ YouTube Video Ready\n\n"
            "🎬 Select Clip Duration",
            reply_markup=duration_keyboard()
        )

    except Exception as e:

        await status.edit_text(
            f"❌ Download Failed\n\n{e}"
        )
