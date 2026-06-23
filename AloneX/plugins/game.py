import random
from pyrogram import filters, types
from AloneX import pbot as bot
from AloneX.db.game import (
    register_user,
    get_cash,
    update_cash,
    update_name,
    update_kills,
    get_kills,
    set_protection,
    get_protection,
    get_profile,
    get_richlist,
    add_bank,
    remove_bank,
    get_bank,
    update_bank
)
from datetime import datetime, timedelta

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
@bot.on_message(filters.command("kill"))
async def kill(_, m: types.Message):

    await register_user(
        m.from_user.id,
        m.from_user.full_name
    )

    if not m.reply_to_message:
        return await m.reply(
            "❌ Reply to a target user."
        )

    killer = m.from_user
    victim = m.reply_to_message.from_user
    protection = await get_protection(
    victim.id
    )

    if protection:
        if protection > datetime.now().timestamp():
            return await m.reply(
                "🛡 Target is protected."
            )

    if victim.id == killer.id:
        return await m.reply(
            "❌ You can't kill yourself."
        )

    victim_cash = await get_cash(
        victim.id
    )

    reward = victim_cash + 100

    await update_cash(
        victim.id,
        -victim_cash
    )

    await update_cash(
        killer.id,
        reward
    )

    await update_kills(
        killer.id
    )

    kills = await get_kills(
        killer.id
    )

    await m.reply(
        f"☠️ KILL SUCCESSFUL\n\n"
        f"👤 Victim: {victim.mention}\n"
        f"💰 Looted: {victim_cash}\n"
        f"🎁 Bonus: 100\n"
        f"🏆 Total Kills: {kills}"
    )
@bot.on_message(filters.command("kills"))
async def kills(_, m: types.Message):

    await register_user(
        m.from_user.id,
        m.from_user.full_name
    )

    total = await get_kills(
        m.from_user.id
    )

    await m.reply(
        f"☠️ Total Kills: {total}"
        )
@bot.on_message(filters.command("rob"))
async def rob(_, m: types.Message):

    await register_user(
        m.from_user.id,
        m.from_user.full_name
    )

    if not m.reply_to_message:
        return await m.reply(
            "❌ Reply to a target user."
        )

    if len(m.command) < 2:
        return await m.reply(
            "Usage: /rob 1000"
        )

    try:
        amount = int(m.command[1])
    except:
        return await m.reply(
            "❌ Invalid amount."
        )

    robber = m.from_user
    victim = m.reply_to_message.from_user
    protection = await get_protection(
    victim.id
    )

    if protection:
        if protection > datetime.now().timestamp():
            return await m.reply(
            "🛡 Target is protected."
            )

    if victim.id == robber.id:
        return await m.reply(
            "❌ You can't rob yourself."
        )

    victim_cash = await get_cash(
        victim.id
    )

    if victim_cash < amount:
        return await m.reply(
            f"❌ User only has {victim_cash} cash."
        )

    success = random.randint(1, 100)

    if success <= 60:

        await update_cash(
            victim.id,
            -amount
        )

        await update_cash(
            robber.id,
            amount
        )

        await m.reply(
            f"🦹 ROB SUCCESSFUL\n\n"
            f"💰 Stolen: {amount}"
        )

    else:

        fine = 500

        await update_cash(
            robber.id,
            -fine
        )

        await m.reply(
            f"🚔 ROB FAILED\n\n"
            f"💸 Fine: {fine}"
        )
@bot.on_message(filters.command("roball"))
async def rob_all(_, m: types.Message):

    await register_user(
        m.from_user.id,
        m.from_user.full_name
    )

    if not m.reply_to_message:
        return await m.reply(
            "Reply to a target."
        )

    victim = m.reply_to_message.from_user

    victim_cash = await get_cash(
        victim.id
    )

    if victim_cash <= 0:
        return await m.reply(
            "Victim is broke."
        )

    percentage = random.randint(25, 75)

    loot = int(
        victim_cash * percentage / 100
    )

    await update_cash(
        victim.id,
        -loot
    )

    await update_cash(
        m.from_user.id,
        loot
    )

    await m.reply(
        f"💀 ROB ALL SUCCESS\n\n"
        f"💰 Looted: {loot}\n"
        f"📊 {percentage}% stolen"
    )
@bot.on_message(filters.command("protect"))
async def protect(_, m: types.Message):

    await register_user(
        m.from_user.id,
        m.from_user.full_name
    )

    if len(m.command) < 2:
        return await m.reply(
            "Usage:\n/protect 1D\n/protect 2D\n/protect 3D"
        )

    plan = m.command[1].upper()

    prices = {
        "1D": (1, 1000),
        "2D": (2, 1800),
        "3D": (3, 2500)
    }

    if plan not in prices:
        return await m.reply(
            "Available Plans:\n1D\n2D\n3D"
        )

    days, cost = prices[plan]

    cash = await get_cash(
        m.from_user.id
    )

    if cash < cost:
        return await m.reply(
            f"❌ Need {cost} cash."
        )

    await update_cash(
        m.from_user.id,
        -cost
    )

    expiry = (
        datetime.now() +
        timedelta(days=days)
    ).timestamp()

    await set_protection(
        m.from_user.id,
        expiry
    )

    await m.reply(
        f"🛡 Protection Activated\n\n"
        f"Plan: {plan}\n"
        f"Cost: {cost}"
    )
@bot.on_message(filters.command("shield"))
async def shield(_, m: types.Message):

    protection = await get_protection(
        m.from_user.id
    )

    if not protection:
        return await m.reply(
            "❌ No active protection."
        )

    left = int(
        protection -
        datetime.now().timestamp()
    )

    if left <= 0:
        return await m.reply(
            "❌ Protection expired."
        )

    hours = left // 3600

    await m.reply(
        f"🛡 Protection Active\n\n"
        f"⏰ Remaining: {hours} hours"
    )
@bot.on_message(filters.command("bank"))
async def bank(_, m: types.Message):

    await register_user(
        m.from_user.id,
        m.from_user.full_name
    )

    cash = await get_cash(
        m.from_user.id
    )

    bank_cash = await get_bank(
        m.from_user.id
    )

    await m.reply(
        f"🏦 BANK ACCOUNT\n\n"
        f"💵 Cash: {cash}\n"
        f"🏦 Bank: {bank_cash}"
    )
@bot.on_message(filters.command("deposit"))
async def deposit(_, m: types.Message):

    if len(m.command) < 2:
        return await m.reply(
            "Usage: /deposit amount"
        )

    amount = int(m.command[1])

    cash = await get_cash(
        m.from_user.id
    )

    if amount > cash:
        return await m.reply(
            "❌ Not enough cash."
        )

    await update_cash(
        m.from_user.id,
        -amount
    )

    await update_bank(
        m.from_user.id,
        amount
    )

    await m.reply(
        f"🏦 Deposited {amount} Cash"
    )
@bot.on_message(filters.command("withdraw"))
async def withdraw(_, m: types.Message):

    if len(m.command) < 2:
        return await m.reply(
            "Usage: /withdraw amount"
        )

    amount = int(m.command[1])

    bank_cash = await get_bank(
        m.from_user.id
    )

    if amount > bank_cash:
        return await m.reply(
            "❌ Not enough bank balance."
        )

    await update_bank(
        m.from_user.id,
        -amount
    )

    await update_cash(
        m.from_user.id,
        amount
    )

    await m.reply(
        f"💰 Withdrawn {amount} Cash"
    )
@bot.on_message(filters.command("richlist"))
async def richlist(client, message):

    users = await get_richlist(10)

    text = "💰 TOP RICH USERS\n\n"

    for i, user in enumerate(users, 1):
        text += f"{i}. {user.get('name','Unknown')} - {user.get('cash',0)}\n"

    await message.reply(text)
@bot.on_message(filters.command("beg"))
async def beg(_, m: types.Message):

    reward = random.randint(
        50,
        500
    )

    await update_cash(
        m.from_user.id,
        reward
    )

    await m.reply(
        f"🥺 Someone gave you {reward} Cash!"
    ) 
@bot.on_message(filters.command("flip"))
async def flip(_, m: types.Message):

    if len(m.command) < 2:
        return await m.reply(
            "Usage: /flip amount"
        )

    amount = int(m.command[1])

    cash = await get_cash(
        m.from_user.id
    )

    if amount > cash:
        return await m.reply(
            "❌ Not enough cash."
        )

    win = random.choice(
        [True, False]
    )

    if win:

        await update_cash(
            m.from_user.id,
            amount
        )

        await m.reply(
            f"🪙 You Won {amount}!"
        )

    else:

        await update_cash(
            m.from_user.id,
            -amount
        )

        await m.reply(
            f"💀 You Lost {amount}!"
        )
@bot.on_message(filters.command("profile"))
async def profile(client, message):

    user_id = message.from_user.id

    user = await get_profile(user_id)

    if not user:
        await message.reply("❌ Profile not found")
        return

    await message.reply(
        f"""
👤 Name: {user['name']}
💰 Cash: {user['cash']}
🏦 Bank: {user['bank']}
🔪 Kills: {user['kills']}
"""
        )
@bot.on_message(filters.command("bonus"))
async def bonus(_, m):

    reward = random.randint(
        100,
        2000
    )

    await update_cash(
        m.from_user.id,
        reward
    )

    await m.reply(
        f"🎁 Bonus Reward\n\n"
        f"💰 +{reward}"
    )
@bot.on_message(filters.command("mine"))
async def mine(_, m):

    reward = random.randint(
        500,
        5000
    )

    await update_cash(
        m.from_user.id,
        reward
    )

    await m.reply(
        f"⛏ Mining Success\n\n"
        f"💰 Found: {reward}"
    )
@bot.on_message(filters.command("fish"))
async def fish(_, m):

    reward = random.randint(
        200,
        3000
    )

    await update_cash(
        m.from_user.id,
        reward
    )

    await m.reply(
        f"🎣 Fishing Success\n\n"
        f"💰 Earned: {reward}"
    )
@bot.on_message(filters.command("hunt"))
async def hunt(_, m):

    reward = random.randint(
        1000,
        7000
    )

    await update_cash(
        m.from_user.id,
        reward
    )

    await m.reply(
        f"🏹 Hunting Success\n\n"
        f"💰 Reward: {reward}"
    )
@bot.on_message(filters.command("xo"))
async def xo(_, m):
    await m.reply("🎮 XO Command Working!")
