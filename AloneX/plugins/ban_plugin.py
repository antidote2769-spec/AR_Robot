from AloneX import app
from pyrogram.types import Message
from AloneX.db.ban_db import ban_user, unban_user, is_banned

OWNER_ID = 8773888974


@app.on_message(filters.command("notuse"))
async def ban_cmd(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return

    if len(message.command) < 2:
        return await message.reply("❌ Use: /notuse user_id")

    user_id = int(message.command[1])

    await ban_user(user_id)

    await message.reply(f"🚫 Banned: `{user_id}`")


@app.on_message(filters.command("use"))
async def unban_cmd(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return

    if len(message.command) < 2:
        return await message.reply("❌ Use: /use user_id")

    user_id = int(message.command[1])

    await unban_user(user_id)

    await message.reply(f"✅ Unbanned: `{user_id}`")


@app.on_message(filters.all & ~filters.me)
async def ban_checker(client: Client, message: Message):
    if not message.from_user:
        return

    if await is_banned(message.from_user.id):
        await message.reply_text(
            "🚫 ACCESS DENIED\nYou are banned from using this bot."
        )
        return
