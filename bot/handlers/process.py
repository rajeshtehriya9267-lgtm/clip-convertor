from aiogram import Router
from aiogram.types import FSInputFile, Message

from bot.ai.highlights import generate_highlight_timestamps
from bot.video.clipper import create_clip

router = Router()


async def process_video(
    message: Message,
    video_path: str,
    clip_duration: int,
    total_clips: int
):

    status = await message.answer(
        "🤖 Analyzing video..."
    )

    timestamps = generate_highlight_timestamps(
        video_path,
        total_clips
    )

    await status.edit_text(
        "✂️ Creating clips..."
    )

    created_clips = []

    for timestamp in timestamps:

        clip_path = create_clip(
            video_path,
            timestamp,
            clip_duration
        )

        created_clips.append(clip_path)

    await status.edit_text(
        f"📤 Sending {len(created_clips)} clips..."
    )

    for clip in created_clips:

        video = FSInputFile(clip)

        await message.answer_video(
            video=video
        )

    await status.edit_text(
        "✅ Done!"
    )
