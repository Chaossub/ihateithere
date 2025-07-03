import json
import os
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from handlers.utils import is_admin_or_owner, admin_only

# Path for warns JSON
WARNS_PATH = "warns.json"
MUTES_PATH = "mutes.json"

def load_json(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("{}")
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_warns(chat_id, user_id):
    warns = load_json(WARNS_PATH)
    return warns.get(str(chat_id), {}).get(str(user_id), 0)

def set_warns(chat_id, user_id, count):
    warns = load_json(WARNS_PATH)
    chat_id, user_id = str(chat_id), str(user_id)
    if chat_id not in warns:
        warns[chat_id] = {}
    warns[chat_id][user_id] = count
    save_json(WARNS_PATH, warns)

def reset_warns(chat_id, user_id):
    warns = load_json(WARNS_PATH)
    chat_id, user_id = str(chat_id), str(user_id)
    if chat_id in warns and user_id in warns[chat_id]:
        del warns[chat_id][user_id]
        save_json(WARNS_PATH, warns)

# --- Mute logic (track unmute times) ---
def add_mute(chat_id, user_id, until=None):
    mutes = load_json(MUTES_PATH)
    chat_id, user_id = str(chat_id), str(user_id)
    if chat_id not in mutes:
        mutes[chat_id] = {}
    mutes[chat_id][user_id] = until
    save_json(MUTES_PATH, mutes)

def remove_mute(chat_id, user_id):
    mutes = load_json(MUTES_PATH)
    chat_id, user_id = str(chat_id), str(user_id)
    if chat_id in mutes and user_id in mutes[chat_id]:
        del mutes[chat_id][user_id]
        save_json(MUTES_PATH, mutes)

def get_mute(chat_id, user_id):
    mutes = load_json(MUTES_PATH)
    return mutes.get(str(chat_id), {}).get(str(user_id), None)

# --- Command handlers ---

def register(app):

    @app.on_message(filters.command("warn") & filters.group)
    @admin_only
    async def warn_handler(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user's message to warn them.")
            return
        user = message.reply_to_message.from_user
        chat_id = message.chat.id

        count = get_warns(chat_id, user.id) + 1
        set_warns(chat_id, user.id, count)
        await message.reply(f"⚠️ {user.mention} has been warned! ({count}/6)")

        # Auto-mute logic
        if count == 3:
            await mute_user(client, chat_id, user.id, 300, message)
        elif count == 6:
            await mute_user(client, chat_id, user.id, 600, message)

    @app.on_message(filters.command("warns") & filters.group)
    @admin_only
    async def warns_handler(client, message: Message):
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            await message.reply("Reply to a user to check their warning count.")
            return
        warns = get_warns(message.chat.id, user.id)
        await message.reply(f"⚠️ {user.mention} has {warns} warnings.")

    @app.on_message(filters.command("resetwarns") & filters.group)
    @admin_only
    async def resetwarns_handler(client, message: Message):
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            await message.reply("Reply to a user to reset their warnings.")
            return
        reset_warns(message.chat.id, user.id)
        await message.reply(f"✅ {user.mention}'s warnings have been reset.")

    @app.on_message(filters.command("mute") & filters.group)
    @admin_only
    async def mute_handler(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user's message to mute them.")
            return
        user = message.reply_to_message.from_user
        chat_id = message.chat.id

        # Mute time in seconds (optional arg)
        args = message.text.split()
        seconds = None
        if len(args) > 1 and args[1].isdigit():
            seconds = int(args[1])
        await mute_user(client, chat_id, user.id, seconds, message)

    async def mute_user(client, chat_id, user_id, seconds, message):
        until_date = None
        if seconds:
            until_date = int(message.date.timestamp()) + seconds
        try:
            await client.restrict_chat_member(
                chat_id,
                user_id,
                permissions=0,
                until_date=until_date
            )
            add_mute(chat_id, user_id, until_date)
            if seconds:
                await message.reply(f"🔇 User muted for {seconds//60 if seconds >= 60 else seconds} {'minutes' if seconds and seconds >= 60 else 'seconds'}.")
            else:
                await message.reply("🔇 User muted indefinitely.")
            # Auto-unmute after time, if timed
            if seconds:
                await asyncio.sleep(seconds)
                await client.unban_chat_member(chat_id, user_id)
                remove_mute(chat_id, user_id)
                await message.reply(f"🔊 User <a href='tg://user?id={user_id}'>unmuted</a> automatically.")
        except Exception as e:
            await message.reply(f"Failed to mute: {e}")

    @app.on_message(filters.command("unmute") & filters.group)
    @admin_only
    async def unmute_handler(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user's message to unmute them.")
            return
        user = message.reply_to_message.from_user
        chat_id = message.chat.id
        try:
            await client.unban_chat_member(chat_id, user.id)
            remove_mute(chat_id, user.id)
            await message.reply(f"🔊 {user.mention} has been unmuted.")
        except Exception as e:
            await message.reply(f"Failed to unmute: {e}")

    @app.on_message(filters.command("kick") & filters.group)
    @admin_only
    async def kick_handler(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user's message to kick them.")
            return
        user = message.reply_to_message.from_user
        chat_id = message.chat.id
        try:
            await client.kick_chat_member(chat_id, user.id)
            await message.reply(f"👢 {user.mention} has been kicked from the group.")
        except Exception as e:
            await message.reply(f"Failed to kick: {e}")

    @app.on_message(filters.command("ban") & filters.group)
    @admin_only
    async def ban_handler(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user's message to ban them.")
            return
        user = message.reply_to_message.from_user
        chat_id = message.chat.id
        try:
            await client.kick_chat_member(chat_id, user.id)
            await message.reply(f"🚫 {user.mention} has been banned from the group.")
        except Exception as e:
            await message.reply(f"Failed to ban: {e}")

    @app.on_message(filters.command("unban") & filters.group)
    @admin_only
    async def unban_handler(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user's message to unban them.")
            return
        user = message.reply_to_message.from_user
        chat_id = message.chat.id
        try:
            await client.unban_chat_member(chat_id, user.id)
            await message.reply(f"✅ {user.mention} has been unbanned.")
        except Exception as e:
            await message.reply(f"Failed to unban: {e}")

    @app.on_message(filters.command("userinfo") & filters.group)
    @admin_only
    async def userinfo_handler(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user's message to get their info.")
            return
        user = message.reply_to_message.from_user
        warns = get_warns(message.chat.id, user.id)
        await message.reply(
            f"<b>User info:</b>\n"
            f"ID: <code>{user.id}</code>\n"
            f"Name: {user.mention}\n"
            f"Warnings: <code>{warns}</code>"
        )

    # Flirty warn (doesn't count toward warnings/mute)
    @app.on_message(filters.command("flirtywarn") & filters.group)
    @admin_only
    async def flirtywarn_handler(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user's message to send a flirty warning.")
            return
        user = message.reply_to_message.from_user
        import random
        responses = [
            f"{user.mention}, you’re being so naughty... 😈",
            f"Careful {user.mention}, or you’ll have me blushing! 😘",
            f"{user.mention}, do you want extra attention from the mods? 😉",
            f"Such a tease, {user.mention}... don’t tempt me!",
            f"Flirty warning for {user.mention}! Someone likes to break the rules in style...",
            f"{user.mention}, this is your flirty warning. Behave... or don’t. 😏",
            f"Hey {user.mention}, are you always this much trouble?",
            f"Naughty, naughty {user.mention}! But I’ll let it slide… this time.",
            f"{user.mention}, you’re pushing my buttons in all the right ways.",
            f"{user.mention}, you just earned a wink from the mods. Keep it up 😏",
        ]
        await message.reply(random.choice(responses))
