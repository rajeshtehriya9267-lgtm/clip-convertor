import os
import uuid

DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def download_telegram_video(bot, video):

    file = await bot.get_file(video.file_id)

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    await bot.download_file(
        file.file_path,
        destination=filepath
    )

    return filepath
