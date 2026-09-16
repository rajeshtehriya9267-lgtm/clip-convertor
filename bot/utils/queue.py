import asyncio

processing_users = set()


async def acquire_user(user_id: int):

    if user_id in processing_users:
        return False

    processing_users.add(user_id)

    return True


async def release_user(user_id: int):

    processing_users.discard(user_id)
