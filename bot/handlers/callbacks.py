from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from bot.handlers.process import process_video

router = Router()

user_settings = {}
video_storage = {}


@router.callback_query(F.data.startswith("duration_"))
async def duration_callback(callback: CallbackQuery):

    user_id = callback.from_user.id

    duration = int(
        callback.data.split("_")[1]
    )

    user_settings[user_id] = {
        "duration": duration
    }

    await callback.message.edit_text(
        f"✅ Duration Selected: {duration}s\n\n"
        "✍️ Send clip count (Example: 3, 5, 10)"
    )

    await callback.answer()


@router.message(lambda m: m.text and m.text.isdigit())
async def clip_count_handler(message: Message):

    user_id = message.from_user.id

    if user_id not in user_settings:
        return

    if user_id not in video_storage:
        await message.answer(
            "❌ Send a video first."
        )
        return

    clips = int(message.text)

    if clips < 1 or clips > 20:
        await message.answer(
            "❌ Clip count must be between 1 and 20."
        )
        return

    duration = user_settings[user_id]["duration"]

    video_path = video_storage[user_id]

    await process_video(
        message,
        video_path,
        duration,
        clips
    )
