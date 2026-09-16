from aiogram.types import Message, FSInputFile

from bot.ai.highlights import generate_highlight_timestamps
from bot.video.clipper import create_clip
from bot.utils.cleanup import safe_delete
from bot.utils.queue import acquire_user, release_user


async def process_video(
    message: Message,
    video_path: str,
    clip_duration: int,
    total_clips: int
):

    user_id = message.from_user.id

    allowed = await acquire_user(user_id)

    if not allowed:
        await message.answer(
            "⏳ Your previous task is still processing."
        )
        return

    status = await message.answer(
        "🔍 Analyzing video... 10%"
    )

    created_clips = []

    try:

        timestamps = generate_highlight_timestamps(
            video_path,
            total_clips
        )

        if not timestamps:
            await status.edit_text(
                "❌ No highlights found."
            )
            await release_user(user_id)
            return

        await status.edit_text(
            "🤖 Highlights found... 30%"
        )

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
                f"✂️ Creating clips... {progress}%"
            )

        await status.edit_text(
            "📤 Uploading clips... 90%"
        )

        for clip in created_clips:

            await message.answer_video(
                video=FSInputFile(clip),
                caption="🎬 Generated Highlight Clip"
            )

        await status.edit_text(
            "✅ Completed 100%"
        )

    except Exception as error:

        await status.edit_text(
            f"❌ Error:\n{error}"
        )

    finally:

        safe_delete(video_path)

        for clip in created_clips:
            safe_delete(clip)

        await release_user(user_id)
