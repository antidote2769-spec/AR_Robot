from pyrogram import Client, filters, StopPropagation
from AloneX.db.ban_db import ban_user, unban_user, is_banned

OWNER_ID = 8773888974

@Client.on_message(filters.command("notuse"))
async def notuse_cmd(client, message):
    if not message.from_user or message.from_user.id != OWNER_ID:
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Usage:\n/notuse user_id"
        )

    try:
        user_id = int(message.command[1])

        await ban_user(user_id)

        check = await is_banned(user_id)

        if check:
            await message.reply_text(
                f"🚫 User `{user_id}` has been banned successfully."
            )
        else:
            await message.reply_text(
                "❌ Failed to ban user."
            )

    except Exception as e:
        await message.reply_text(f"❌ Error:\n{e}")


@Client.on_message(filters.command("use"))
async def use_cmd(client, message):
    if not message.from_user or message.from_user.id != OWNER_ID:
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
        await message.reply_text(f"❌ Error:\n{e}")


@Client.on_message(filters.all, group=-1)
async def ban_check(client, message):
    if not message.from_user:
        return

    banned = await is_banned(message.from_user.id)

    if banned:
        await message.reply_text(
            "🚫 **ACCESS DENIED**\n\n"
            "You are banned from using AR_XBOT.\n"
            "Contact bot owner for support."
        )
        raise StopPropagation
