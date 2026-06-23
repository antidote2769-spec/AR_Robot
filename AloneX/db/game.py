
from AloneX import database2 as database

db = database['game']


async def delete_data(user_id: int) -> bool:
       user_filter = {"user_id": user_id}
       await db.delete_one(user_filter)
       return True

async def update_cash(user_id: int, cash: int = 0) -> bool:
       user_filter = {"user_id": user_id}
       cash_update = {"$inc": {"cash": cash}}
       okay = await db.update_one(user_filter, cash_update, upsert=True)
       return True


async def get_cash(user_id: int) -> int:
      user_filter = {"user_id": user_id}
      user = await db.find_one(user_filter)
      return user.get('cash', 0) if user else 0
      
async def get_steal_date(user_id: int, target_user_id: int) -> int:
    user_filter = {"user_id": user_id}
    user = await db.find_one(user_filter)
    return user.get("users", {}).get(str(target_user_id)) if user else None

async def update_steal_date(user_id: int, target_user_id: int, steal_date: int) -> bool:
    user_filter = {"user_id": user_id}
    steal_filter = {"$set": {f"users.{target_user_id}": steal_date}}
    okay = await db.update_one(user_filter, steal_filter)
    return True 

async def update_name(user_id: int, name: str) -> bool:
    user_filter = {"user_id": user_id}
    name_filter = {"$set": {"name": name}}
    okay = await db.update_one(user_filter, name_filter)
    return True

async def get_top_users(limit: int = 10):
    top_users = await db.find().sort("cash", -1).limit(limit).to_list(limit)
    return top_users

# =========================
# NEW ECONOMY FUNCTIONS
# =========================

async def register_user(user_id: int, name: str = None):
    user = await db.find_one({"user_id": user_id})

    if not user:
        await db.insert_one(
            {
                "user_id": user_id,
                "name": name,
                "cash": 500,
                "bank": 0,
                "kills": 0,
                "protection": None,
                "daily": 0,
                "work": 0,
                "crime": 0
            }
        )

    return True


async def get_user(user_id: int):
    return await db.find_one({"user_id": user_id})


async def update_bank(user_id: int, amount: int):
    await db.update_one(
        {"user_id": user_id},
        {"$inc": {"bank": amount}},
        upsert=True
    )


async def get_bank(user_id: int):
    user = await db.find_one({"user_id": user_id})

    if not user:
        return 0

    return user.get("bank", 0)


async def update_kills(user_id: int):
    await db.update_one(
        {"user_id": user_id},
        {"$inc": {"kills": 1}},
        upsert=True
    )


async def get_kills(user_id: int):
    user = await db.find_one({"user_id": user_id})

    if not user:
        return 0

    return user.get("kills", 0)


async def set_protection(user_id: int, expiry):
    await db.update_one(
        {"user_id": user_id},
        {"$set": {"protection": expiry}},
        upsert=True
    )


async def get_protection(user_id: int):
    user = await db.find_one({"user_id": user_id})

    if not user:
        return None

    return user.get("protection")
async def update_kills(user_id: int):
    await db.update_one(
        {"user_id": user_id},
        {"$inc": {"kills": 1}},
        upsert=True
    )

async def get_kills(user_id: int):
    user = await db.find_one(
        {"user_id": user_id}
    )

    if not user:
        return 0

    return user.get("kills", 0)
async def set_protection(user_id: int, expiry):
    await db.update_one(
        {"user_id": user_id},
        {"$set": {"protection": expiry}},
        upsert=True
    )

async def get_protection(user_id: int):
    user = await db.find_one({"user_id": user_id})

    if not user:
        return None

    return user.get("protection")
# =========================
# PROFILE & RICHLIST
# =========================

async def get_profile(user_id: int):
    user = await db.find_one({"user_id": user_id})

    if not user:
        return None

    return {
        "name": user.get("name", "Unknown"),
        "cash": user.get("cash", 0),
        "bank": user.get("bank", 0),
        "kills": user.get("kills", 0),
        "protection": user.get("protection")
    }


async def get_richlist(limit: int = 10):
    users = await db.find().sort(
        "cash",
        -1
    ).limit(limit).to_list(length=limit)

    return users       
async def add_bank(user_id: int, amount: int):
    await db.update_one(
        {"user_id": user_id},
        {"$inc": {"bank": amount}},
        upsert=True
    )
    return True


async def remove_bank(user_id: int, amount: int):
    await db.update_one(
        {"user_id": user_id},
        {"$inc": {"bank": -amount}},
        upsert=True
    )
    return True
# =========================
# TIC TAC TOE GAME DATABASE
# =========================

async def create_ttt(game_id, player1, player2="bot"):
    await db.update_one(
        {"game_id": game_id},
        {
            "$set": {
                "game_id": game_id,
                "player1": player1,
                "player2": player2,
                "board": [
                    "⬜","⬜","⬜",
                    "⬜","⬜","⬜",
                    "⬜","⬜","⬜"
                ],
                "turn": player1,
                "status": "playing"
            }
        },
        upsert=True
    )

    return True



async def get_ttt(game_id):
    return await db.find_one(
        {"game_id": game_id}
    )



async def update_ttt(game_id, board, turn):
    await db.update_one(
        {"game_id": game_id},
        {
            "$set": {
                "board": board,
                "turn": turn
            }
        }
    )

    return True



async def delete_ttt(game_id):
    await db.delete_one(
        {"game_id": game_id}
    )

    return True



async def end_ttt(game_id, winner):
    await db.update_one(
        {"game_id": game_id},
        {
            "$set": {
                "status": "ended",
                "winner": winner
            }
        }
    )

    return True
