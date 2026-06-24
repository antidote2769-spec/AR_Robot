from pyrogram import Client, filters
from AloneX.db.ban_db import ban_user, unban_user

OWNER_ID = 8773888974,8871937776  # apna Telegram ID

@Client.on_message(filters.command("notuse") & filters.user(OWNER_ID))
async def notuse_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /notuse user_id")

    user_id = int(message.command[1])
    ban_user(user_id)

    await message.reply_text("🚫 User blocked.")

@Client.on_message(filters.command("use") & filters.user(OWNER_ID))
async def use_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /use user_id")

    user_id = int(message.command[1])
    unban_user(user_id)

    await message.reply_text("✅ User unblocked.")
