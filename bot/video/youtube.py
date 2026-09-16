import os
import uuid
import yt_dlp

DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def download_youtube_video(url: str):

    video_id = str(uuid.uuid4())
    output_path = f"{DOWNLOAD_DIR}/{video_id}.mp4"

    ydl_opts = {
        "format": "mp4/best",
        "outtmpl": output_path,
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path
