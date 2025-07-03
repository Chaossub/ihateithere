import json
import os
import random
from pyrogram import filters
from pyrogram.types import Message
from handlers.utils import admin_only

TRACKED_PATH = "tracked_users.json"

def load_json(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("{}")
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_tracked(chat_id):
    tracked = load_json(TRACKED_PATH)
    return tracked.get(str(chat_id), [])

def add_tracked(chat_id, user_id):
    tracked = load_json(TRACKED_PATH)
    chat_id, user_id = str(chat_id), str(user_id)
    if chat_id not in tracked:
        tracked[chat_id] = []
    if user_id not in tracked[chat_id]:
        tracked[chat_id].append(user_id)
        save_json(TRACKED_PATH, tracked)

def register(app):

    @app.on_message(filters.command("track_all") & filters.group)
    @admin_only
    async def track_all_handler(client, message: Message):
        chat_id = message.chat.id
        tracked = []
        async for member in client.get_chat_members(chat_id):
            if not member.user.is_bot:
                add_tracked(chat_id, member.user.id)
                tracked.append(member.user.id)
        await message.reply(f"Tracking {len(tracked)} members for summoning.")

    @app.on_message(filters.command(["summonall", "flirtysummonall"]) & filters.group)
    async def summon_all_handler(client, message: Message):
        chat_id = message.chat.id
        tracked = get_tracked(chat_id)
        if not tracked:
            await message.reply("No users tracked! Use /track_all first.")
            return
        mentions = [f"<a href='tg://user?id={uid}'>.</a>" for uid in tracked]
        is_flirty = message.command[0] == "flirtysummonall"
        responses = [
            "Summoning everyone! 🌟",
            "You’ve all been summoned!",
            "Get in here, naughty ones!",
            "Time to gather, everyone!",
            "Group cuddle, anyone?",
            "All hands (and tails) on deck!",
            "Flirty roll-call! Everyone show up!"
        ] if not is_flirty else [
            "Everyone, come get a little attention 😏",
            "You know you want to be summoned by me...",
            "All you naughty people, gather round!",
            "I only summon the best—so that's all of you! 😘",
            "Don't make me come looking for you... everyone get in here!",
            "Flirty summon! Hope you can handle it…",
            "The fun starts now—come play!"
        ]
        text = f"{random.choice(responses)}\n" + " ".join(mentions)
        await message.reply(text, disable_web_page_preview=True)

    @app.on_message(filters.command(["summon", "flirtysummon"]) & filters.group)
    async def summon_handler(client, message: Message):
        args = message.text.split()
        is_flirty = message.command[0] == "flirtysummon"
        if len(args) < 2 or not args[1].startswith("@"):
            await message.reply("Usage: /summon @username")
            return
        username = args[1].lstrip("@")
        try:
            user = await client.get_users(username)
        except Exception:
            await message.reply("User not found!")
            return
        add_tracked(message.chat.id, user.id)
        responses = [
            f"Summoning {user.mention}!",
            f"Come here, {user.mention}!",
            f"{user.mention}, you’ve been summoned!",
            f"Hey {user.mention}, we need you here!",
            f"{user.mention}, your presence is requested."
        ] if not is_flirty else [
            f"{user.mention}, I just had to flirty-summon you… 😘",
            f"Hey {user.mention}, you’re too cute not to summon!",
            f"{user.mention}, the group’s not the same without you. Come play! 😏",
            f"I’m summoning you with a wink, {user.mention}.",
            f"{user.mention}, you know you love the attention!"
        ]
        await message.reply(random.choice(responses))

    @app.on_message(filters.command("cancel") & filters.group)
    async def cancel_handler(client, message: Message):
        await message.reply("There’s nothing to cancel, but I appreciate your enthusiasm 😉")
