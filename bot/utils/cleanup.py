import os


def safe_delete(file_path: str):

    try:

        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception:
        pass
