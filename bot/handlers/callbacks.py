from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

user_settings = {}


@router.callback_query(F.data.startswith("duration_"))
async def duration_callback(callback: CallbackQuery):

    user_id = callback.from_user.id
    duration = int(callback.data.split("_")[1])

    if user_id not in user_settings:
        user_settings[user_id] = {}

    user_settings[user_id]["duration"] = duration

    kb = InlineKeyboardBuilder()

    kb.button(text="3 Clips", callback_data="clips_3")
    kb.button(text="5 Clips", callback_data="clips_5")
    kb.button(text="10 Clips", callback_data="clips_10")

    kb.adjust(1)

    await callback.message.edit_text(
        f"✅ Duration Selected: {duration}s\n\n"
        "🎬 Select Number Of Clips",
        reply_markup=kb.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data.startswith("clips_"))
async def clips_callback(callback: CallbackQuery):

    user_id = callback.from_user.id
    clips = int(callback.data.split("_")[1])

    if user_id not in user_settings:
        user_settings[user_id] = {}

    user_settings[user_id]["clips"] = clips

    duration = user_settings[user_id].get("duration", 30)

    await callback.message.edit_text(
        "✅ Settings Saved\n\n"
        f"🎬 Clip Duration: {duration}s\n"
        f"📦 Total Clips: {clips}\n\n"
        "📤 Now send your video or YouTube link."
    )

    await callback.answer()
