from bot.utils.queue import (
    acquire_user,
    release_user
)
from aiogram.types import FSInputFile, Message

from bot.ai.highlights import generate_highlight_timestamps
from bot.video.clipper import create_clip
from bot.utils.cleanup import safe_delete


async def process_video(
    message: Message,
    video_path: str,
    clip_duration: int,
    total_clips: int
):

    status = await message.answer(
        "🔍 Analyzing Video... 10%"
    )

    try:

        timestamps = generate_highlight_timestamps(
            video_path,
            total_clips
        )

        await status.edit_text(
            "🤖 Highlights Found... 30%"
        )

        created_clips = []

        total = len(timestamps)

        for index, timestamp in enumerate(
            timestamps,
            start=1
        ):

            clip_path = create_clip(
                video_path,
                timestamp,
                clip_duration
            )

            created_clips.append(
                clip_path
            )

            progress = int(
                30 + (index / total) * 50
            )

            await status.edit_text(
                f"✂️ Creating Clips... {progress}%"
            )

        await status.edit_text(
            "📤 Uploading Clips... 90%"
        )

        for clip in created_clips:

            await message.answer_video(
                video=FSInputFile(clip)
            )

        await status.edit_text(
            "✅ Completed 100%"
        )

        safe_delete(video_path)

        for clip in created_clips:
            safe_delete(clip)

    except Exception as error:

        await status.edit_text(
            f"❌ Error:\n\n{error}"
        )

        safe_delete(video_path)
