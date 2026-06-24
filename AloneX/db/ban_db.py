from AloneX import database

blocked_users = database.blocked_users

async def ban_user(user_id):
    await blocked_users.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

async def unban_user(user_id):
    await blocked_users.delete_one(
        {"user_id": user_id}
    )

async def is_banned(user_id):
    user = await blocked_users.find_one(
        {"user_id": user_id}
    )
    return bool(user)
