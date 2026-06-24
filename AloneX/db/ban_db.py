from pymongo import MongoClient
from AloneX import mongodb

blocked_users = mongodb.blocked_users

def ban_user(user_id):
    blocked_users.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

def unban_user(user_id):
    blocked_users.delete_one(
        {"user_id": user_id}
    )

def is_banned(user_id):
    return blocked_users.find_one(
        {"user_id": user_id}
    )
