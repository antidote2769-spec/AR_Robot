from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

from db.game import (
    create_ttt,
    get_ttt,
    update_ttt,
    end_ttt
)


def xo_board(board, game_id):

    buttons = []

    for i in range(0, 9, 3):
        buttons.append([
            InlineKeyboardButton(board[i], callback_data=f"xo|{game_id}|{i}"),
            InlineKeyboardButton(board[i+1], callback_data=f"xo|{game_id}|{i+1}"),
            InlineKeyboardButton(board[i+2], callback_data=f"xo|{game_id}|{i+2}")
        ])

    return InlineKeyboardMarkup(buttons)



def winner(board):

    win = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a,b,c in win:
        if board[a] == board[b] == board[c] and board[a] != "⬜":
            return board[a]

    if "⬜" not in board:
        return "Draw"

    return None



@Client.on_message(filters.command("xo"))
async def xo(client, message):

    user = message.from_user.id

    game_id = str(user)

    board = [
        "⬜","⬜","⬜",
        "⬜","⬜","⬜",
        "⬜","⬜","⬜"
    ]


    await create_ttt(
        game_id,
        user,
        "bot"
    )


    await message.reply(
        "❌ You vs 🤖 Bot\n\nYour Turn",
        reply_markup=xo_board(
            board,
            game_id
        )
    )
