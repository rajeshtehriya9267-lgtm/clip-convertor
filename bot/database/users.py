from bot.database.mongo import users


async def save_user(user):

    await users.update_one(
        {"user_id": user.id},
        {
            "$set": {
                "user_id": user.id,
                "first_name": user.first_name,
                "username": user.username
            }
        },
        upsert=True
    )
