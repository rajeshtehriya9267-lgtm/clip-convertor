from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(lambda message: message.video is not None)
async def video_handler(message: Message):

    duration = message.video.duration

    if duration > 1200:
        return await message.answer(
            "❌ Maximum allowed video length is 20 minutes."
        )

    await message.answer(
        "✅ Video received.\n\n"
        "Select clip duration:\n"
        "10s • 15s • 30s • 60s"
    )


@router.message()
async def youtube_handler(message: Message):

    text = message.text or ""

    if (
        "youtube.com" in text
        or "youtu.be" in text
    ):
        await message.answer(
            "🔗 YouTube link received.\n\n"
            "Select clip duration:\n"
            "10s • 15s • 30s • 60s"
        )
