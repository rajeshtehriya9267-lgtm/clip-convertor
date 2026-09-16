import cv2

from bot.video.ffmpeg_utils import get_video_duration


def generate_highlight_timestamps(
    video_path: str,
    total_clips: int
):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30

    frame_count = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    duration = int(frame_count / fps)

    previous_frame = None

    scores = []

    frame_index = 0

    sample_every = int(fps * 5)

    while True:

        success, frame = cap.read()

        if not success:
            break

        if frame_index % sample_every != 0:
            frame_index += 1
            continue

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        if previous_frame is not None:

            diff = cv2.absdiff(
                previous_frame,
                gray
            )

            motion_score = diff.mean()

            timestamp = int(
                frame_index / fps
            )

            scores.append(
                (
                    timestamp,
                    motion_score
                )
            )

        previous_frame = gray

        frame_index += 1

    cap.release()

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    selected = []

    for timestamp, score in scores:

        if all(
            abs(timestamp - t) > 30
            for t in selected
        ):
            selected.append(timestamp)

        if len(selected) >= total_clips:
            break

    selected.sort()

    if not selected:

        step = duration // (
            total_clips + 1
        )

        selected = [
            step * i
            for i in range(
                1,
                total_clips + 1
            )
        ]

    return selected
