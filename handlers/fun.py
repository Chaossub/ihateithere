import json
import os
import random
from pyrogram import filters
from pyrogram.types import Message

XP_PATH = "xp.json"

def load_json(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("{}")
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_xp(chat_id, user_id):
    xp = load_json(XP_PATH)
    return xp.get(str(chat_id), {}).get(str(user_id), 0)

def add_xp(chat_id, user_id, amount):
    xp = load_json(XP_PATH)
    chat_id, user_id = str(chat_id), str(user_id)
    if chat_id not in xp:
        xp[chat_id] = {}
    if user_id not in xp[chat_id]:
        xp[chat_id][user_id] = 0
    xp[chat_id][user_id] += amount
    save_json(XP_PATH, xp)

def leaderboard(chat_id):
    xp = load_json(XP_PATH)
    chat_id = str(chat_id)
    if chat_id not in xp:
        return []
    items = [(int(uid), score) for uid, score in xp[chat_id].items()]
    items.sort(key=lambda x: x[1], reverse=True)
    return items[:10]

def register(app):
    # /naughty command
    @app.on_message(filters.command("naughty") & filters.group)
    async def naughty_handler(client, message: Message):
        user = message.from_user
        xp = get_xp(message.chat.id, user.id)
        await message.reply(f"😈 {user.mention}, your Naughty XP is: <b>{xp}</b>")

    # /leaderboard command
    @app.on_message(filters.command("leaderboard") & filters.group)
    async def leaderboard_handler(client, message: Message):
        leaders = leaderboard(message.chat.id)
        if not leaders:
            await message.reply("Nobody is naughty yet!")
            return
        text = "<b>Naughtiest Members:</b>\n"
        for i, (uid, score) in enumerate(leaders, 1):
            mention = f"<a href='tg://user?id={uid}'>User {uid}</a>"
            text += f"{i}. {mention}: <b>{score}</b> XP\n"
        await message.reply(text)

    # /tease command
    @app.on_message(filters.command("tease") & filters.group)
    async def tease_handler(client, message: Message):
        user = message.from_user
        add_xp(message.chat.id, user.id, 3)
        responses = [
            f"{user.mention} teases the group... gaining 3 Naughty XP! 😉",
            f"{user.mention} can't resist teasing everyone. Naughty XP up!",
            f"A little tease never hurt anyone, right {user.mention}? +3 XP!",
            f"{user.mention} is dangerously playful... Naughty XP increased!",
            f"Everyone's a little more distracted thanks to {user.mention}... +3 XP."
        ]
        await message.reply(random.choice(responses))

    # /spank command
    @app.on_message(filters.command("spank") & filters.group)
    async def spank_handler(client, message: Message):
        user = message.from_user
        add_xp(message.chat.id, user.id, 5)
        responses = [
            f"{user.mention} delivers a playful spank! +5 Naughty XP! 🍑",
            f"Spank attack! {user.mention} earns 5 XP.",
            f"Naughty! {user.mention} gets bolder with each spank. +5 XP.",
            f"{user.mention} is getting in trouble... Spank received, XP up!",
            f"The room just got hotter. Thank {user.mention} for the spank! +5 XP."
        ]
        await message.reply(random.choice(responses))

    # /bite command
    @app.on_message(filters.command("bite") & filters.group)
    async def bite_handler(client, message: Message):
        user = message.from_user
        add_xp(message.chat.id, user.id, 4)
        responses = [
            f"{user.mention} bites into the fun! +4 Naughty XP. 🦇",
            f"Ouch! {user.mention} is a biter... and naughtier. +4 XP.",
            f"{user.mention} takes a playful bite. Naughty meter rising!",
            f"Biting is encouraged here, right {user.mention}? +4 XP.",
            f"{user.mention} couldn't resist a taste. +4 XP added!"
        ]
        await message.reply(random.choice(responses))

