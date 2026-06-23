import random
from pyrogram import filters, types
from AloneX import pbot as bot
from AloneX.db.game import (
    register_user,
    get_cash,
    update_cash,
    update_name,
    update_kills,
    get_kills
)

__module__ = "Games 🎮"

__help__ = """
💰 Economy System

/bal - Check Balance
"""
@bot.on_message(filters.command(["bal", "balance"]))
async def balance(_, m: types.Message):

    await register_user(
        m.from_user.id,
        m.from_user.full_name
    )

    await update_name(
        m.from_user.id,
        m.from_user.full_name
    )

    cash = await get_cash(m.from_user.id)

    await m.reply(
        f"💰 Balance\n\n"
        f"💸 Cash: {cash}"
    )
@bot.on_message(filters.command("daily"))
async def daily(_, m: types.Message):

    await register_user(
        m.from_user.id,
        m.from_user.full_name
    )

    reward = random.randint(500, 5000)

    await update_cash(
        m.from_user.id,
        reward
    )

    await m.reply(
        f"🎁 Daily Reward\n\n"
        f"💸 +{reward} Cash"
    ) 
@bot.on_message(filters.command("work"))
async def work(_, m: types.Message):

    await register_user(
        m.from_user.id,
        m.from_user.full_name
    )

    reward = random.randint(200, 3000)

    await update_cash(
        m.from_user.id,
        reward
    )

    await m.reply(
        f"👨‍💻 Work Completed\n\n"
        f"💰 Earned: {reward}"
    )
@bot.on_message(filters.command("crime"))
async def crime(_, m: types.Message):

    await register_user(
        m.from_user.id,
        m.from_user.full_name
    )

    success = random.choice([True, False])

    if success:

        reward = random.randint(1000, 7000)

        await update_cash(
            m.from_user.id,
            reward
        )

        await m.reply(
            f"😈 Crime Successful\n\n"
            f"💰 Loot: {reward}"
        )

    else:

        fine = random.randint(500, 3000)

        await update_cash(
            m.from_user.id,
            -fine
        )

        await m.reply(
            f"🚔 Police Caught You\n\n"
            f"💸 Fine: {fine}"
        )   
@bot.on_message(filters.command("give"))
async def give(_, m: types.Message):

    await register_user(
        m.from_user.id,
        m.from_user.full_name
    )

    if not m.reply_to_message:
        return await m.reply(
            "❌ Reply to a user."
        )

    if len(m.command) < 2:
        return await m.reply(
            "Usage: /give 1000"
        )

    amount = int(m.command[1])

    sender = m.from_user
    receiver = m.reply_to_message.from_user

    sender_cash = await get_cash(
        sender.id
    )

    if sender_cash < amount:
        return await m.reply(
            "❌ Not enough cash."
        )

    await update_cash(
        sender.id,
        -amount
    )

    await update_cash(
        receiver.id,
        amount
    )

    await m.reply(
        f"✅ Transfer Successful\n\n"
        f"💸 Sent: {amount}"
    )
