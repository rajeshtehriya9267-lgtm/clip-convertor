import subprocess
import json


def get_video_duration(filepath: str) -> int:

    command = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        filepath
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    data = json.loads(result.stdout)

    return int(float(data["format"]["duration"]))
