import os
import uuid
import subprocess

CLIPS_DIR = "clips"

os.makedirs(CLIPS_DIR, exist_ok=True)


def create_clip(
    input_file: str,
    start_time: int,
    clip_duration: int
):

    output_file = os.path.join(
        CLIPS_DIR,
        f"{uuid.uuid4()}.mp4"
    )

    command = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start_time),
        "-i",
        input_file,
        "-t",
        str(clip_duration),
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        output_file
    ]

    subprocess.run(
        command,
        capture_output=True
    )

    return output_file
