from aiogram import Router, F
from aiogram.types import CallbackQuery

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

    if user_id not in user_settings:
        user_settings[user_id] = {}

    user_settings[user_id]["duration"] = duration

    from aiogram.utils.keyboard import InlineKeyboardBuilder

    kb = InlineKeyboardBuilder()

    kb.button(
        text="3 Clips",
        callback_data="clips_3"
    )

    kb.button(
        text="5 Clips",
        callback_data="clips_5"
    )

    kb.button(
        text="10 Clips",
        callback_data="clips_10"
    )

    kb.adjust(1)

    await callback.message.edit_text(
        f"✅ Duration: {duration}s\n\n"
        "🎬 Select Number Of Clips",
        reply_markup=kb.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data.startswith("clips_"))
async def clips_callback(callback: CallbackQuery):

    user_id = callback.from_user.id

    clips = int(
        callback.data.split("_")[1]
    )

    if user_id not in user_settings:
        user_settings[user_id] = {}

    user_settings[user_id]["clips"] = clips

    duration = user_settings[user_id].get(
        "duration",
        30
    )

    video_path = video_storage.get(user_id)

    if not video_path:

        await callback.message.edit_text(
            "❌ No video found.\n\nSend a video first."
        )

        return

    await callback.message.edit_text(
        "🚀 Processing Started..."
    )

    await process_video(
        callback.message,
        video_path,
        duration,
        clips
    )

    await callback.answer()
