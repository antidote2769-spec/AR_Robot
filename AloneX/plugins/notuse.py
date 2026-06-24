from pyrogram import Client, filters
from AloneX.db.ban_db import ban_user, unban_user

OWNER_ID = 8773888974  # Apna Telegram User ID

@Client.on_message(filters.command("notuse") & filters.user(OWNER_ID))
async def notuse_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/notuse user_id"
        )

    try:
        user_id = int(message.command[1])
        await ban_user(user_id)

        await message.reply_text(
            f"🚫 User {user_id} blocked successfully."
        )
    except Exception as e:
        await message.reply_text(f"Error: {e}")


@Client.on_message(filters.command("use") & filters.user(OWNER_ID))
async def use_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/use user_id"
        )

    try:
        user_id = int(message.command[1])
        await unban_user(user_id)

        await message.reply_text(
            f"✅ User {user_id} unblocked successfully."
        )
    except Exception as e:
        await message.reply_text(f"Error: {e}")
from AloneX.db.ban_db import is_banned
from pyrogram import StopPropagation

@Client.on_message(filters.all, group=-1)
async def ban_check(client, message):
    if not message.from_user:
        return

    if await is_banned(message.from_user.id):
        raise StopPropagation        
