import json
import os
from pyrogram import filters
from pyrogram.types import Message
from handlers.utils import admin_only, mute, unmute, get_warns, add_warn, reset_warns, save_warns

WARN_FILE = "data/warnings.json"
os.makedirs("data", exist_ok=True)

def load_warns():
    if not os.path.isfile(WARN_FILE):
        return {}
    with open(WARN_FILE, "r") as f:
        return json.load(f)

warn_data = load_warns()

def register(app):

    @app.on_message(filters.command("warn") & filters.group)
    @admin_only
    async def warn_user(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to warn them.")
            return

        user_id = str(message.reply_to_message.from_user.id)
        chat_id = str(message.chat.id)

        warns = add_warn(warn_data, chat_id, user_id)
        save_warns(warn_data)

        await message.reply(f"⚠️ Warned! Total warns: {warns}/6")

        if warns == 3:
            await mute(client, message.chat.id, int(user_id), 5, message)
        elif warns == 6:
            await mute(client, message.chat.id, int(user_id), 10, message)

    @app.on_message(filters.command("warns") & filters.group)
    @admin_only
    async def check_warns(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to check their warns.")
            return

        user_id = str(message.reply_to_message.from_user.id)
        chat_id = str(message.chat.id)
        warns = get_warns(warn_data, chat_id, user_id)
        await message.reply(f"⚠️ User has {warns} warns.")

    @app.on_message(filters.command("resetwarns") & filters.group)
    @admin_only
    async def reset_warn(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to reset their warns.")
            return

        user_id = str(message.reply_to_message.from_user.id)
        chat_id = str(message.chat.id)
        reset_warns(warn_data, chat_id, user_id)
        save_warns(warn_data)
        await message.reply("✅ Warns have been reset.")

    @app.on_message(filters.command("flirtywarn") & filters.group)
    @admin_only
    async def flirty_warn(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to send a flirty warning.")
            return

        responses = [
            "💋 Naughty, naughty... behave or I’ll have to punish you~",
            "😈 That was a warning, darling. You’re playing a dangerous game.",
            "💄 Tread carefully, sweet thing. Next time, there might be consequences~"
        ]
        await message.reply(random.choice(responses))

    @app.on_message(filters.command("mute") & filters.group)
    @admin_only
    async def mute_command(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to mute them.")
            return
        args = message.command
        duration = int(args[1]) if len(args) > 1 and args[1].isdigit() else 0
        await mute(client, message.chat.id, message.reply_to_message.from_user.id, duration, message)

    @app.on_message(filters.command("unmute") & filters.group)
    @admin_only
    async def unmute_command(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to unmute them.")
            return
        await unmute(client, message.chat.id, message.reply_to_message.from_user.id, message)

