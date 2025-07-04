import json
import os
from pyrogram import filters
from pyrogram.types import Message
from handlers.utils import admin_only

XP_FILE = "data/xp.json"

def load_xp():
    if os.path.exists(XP_FILE):
        with open(XP_FILE, "r") as f:
            return json.load(f)
    return {}

def save_xp(data):
    with open(XP_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_xp(chat_id, user_id, amount=1):
    chat_id = str(chat_id)
    user_id = str(user_id)
    data = load_xp()
    if chat_id not in data:
        data[chat_id] = {}
    if user_id not in data[chat_id]:
        data[chat_id][user_id] = 0
    data[chat_id][user_id] += amount
    save_xp(data)
    return data[chat_id][user_id]

def get_xp(chat_id, user_id):
    chat_id = str(chat_id)
    user_id = str(user_id)
    data = load_xp()
    return data.get(chat_id, {}).get(user_id, 0)

def get_leaderboard(chat_id):
    chat_id = str(chat_id)
    data = load_xp()
    return sorted(data.get(chat_id, {}).items(), key=lambda x: x[1], reverse=True)[:10]

def register(app):
    @app.on_message(filters.command("naughty") & filters.group)
    async def show_xp(client, message: Message):
        user_id = message.from_user.id
        chat_id = message.chat.id
        xp = get_xp(chat_id, user_id)
        await message.reply(f"😈 Naughty XP: <b>{xp}</b>")

    @app.on_message(filters.command("leaderboard") & filters.group)
    @admin_only
    async def show_leaderboard(client, message: Message):
        chat_id = message.chat.id
        leaderboard = get_leaderboard(chat_id)
        if not leaderboard:
            await message.reply("No XP data found.")
            return
        text = "🔥 <b>Naughty Leaderboard</b> 🔥\n\n"
        for i, (user_id, xp) in enumerate(leaderboard, start=1):
            text += f"{i}. <a href='tg://user?id={user_id}'>User</a> – {xp} XP\n"
        await message.reply(text)

