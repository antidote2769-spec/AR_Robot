from pyrogram import Client, filters
from AloneX.db.ban_db import ban_user, unban_user, is_banned
from pyrogram import StopPropagation

OWNER_ID = 8773888974  # Apna Telegram ID

@Client.on_message(filters.command("notuse"))
async def notuse_cmd(client, message):
    if message.from_user.id != OWNER_ID:
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Usage:\n/notuse user_id"
        )

    try:
        user_id = int(message.command[1])

        await ban_user(user_id)

        await message.reply_text(
            f"🚫 User `{user_id}` has been banned from using AR_XBOT."
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")


@Client.on_message(filters.command("use"))
async def use_cmd(client, message):
    if message.from_user.id != OWNER_ID:
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Usage:\n/use user_id"
        )

    try:
        user_id = int(message.command[1])

        await unban_user(user_id)

        await message.reply_text(
            f"✅ User `{user_id}` has been unbanned."
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")


@Client.on_message(filters.all, group=-1)
async def ban_check(client, message):
    if not message.from_user:
        return

    print(f"Checking User: {message.from_user.id}")

    if await is_banned(message.from_user.id):
        print(f"BANNED USER DETECTED: {message.from_user.id}")

        await message.reply_text(
            "🚫 You are banned from using AR_XBOT."
        )
        raise StopPropagation
