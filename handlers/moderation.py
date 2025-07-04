import json
import os
from datetime import datetime, timedelta
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from handlers.utils import is_admin_or_owner, admin_only

WARN_FILE = "data/warnings.json"

def load_warnings():
    if not os.path.exists(WARN_FILE):
        return {}
    with open(WARN_FILE, "r") as f:
        return json.load(f)

def save_warnings(data):
    with open(WARN_FILE, "w") as f:
        json.dump(data, f, indent=2)

def register(app):

    # Warn command
    @app.on_message(filters.command("warn") & filters.group)
    @admin_only
    async def warn_user(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to the user's message to warn them.")
            return

        user_id = str(message.reply_to_message.from_user.id)
        chat_id = str(message.chat.id)

        warnings = load_warnings()
        warnings.setdefault(chat_id, {})
        warnings[chat_id][user_id] = warnings[chat_id].get(user_id, 0) + 1
        count = warnings[chat_id][user_id]
        save_warnings(warnings)

        await message.reply(f"⚠️ {message.reply_to_message.from_user.mention} has been warned. Total: {count}")

        # Auto-mute logic
        if count == 3:
            await mute(client, chat_id, user_id, 5, message)
        elif count == 6:
            await mute(client, chat_id, user_id, 10, message)

    # Flirty warn (does not count)
    @app.on_message(filters.command("flirtywarn") & filters.group)
    @admin_only
    async def flirty_warn(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to flirty-warn them.")
            return

        flirty_lines = [
            "You're treading on dangerous ground, cutie 😏",
            "One more slip and I might have to tie you up... in rules, of course 💋",
            "Naughty behavior won't go unnoticed 😈",
        ]
        await message.reply(random.choice(flirty_lines))

    # Reset warnings
    @app.on_message(filters.command("resetwarns") & filters.group)
    @admin_only
    async def reset_warns(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to reset their warnings.")
            return

        user_id = str(message.reply_to_message.from_user.id)
        chat_id = str(message.chat.id)
        warnings = load_warnings()

        if chat_id in warnings and user_id in warnings[chat_id]:
            warnings[chat_id][user_id] = 0
            save_warnings(warnings)
            await message.reply("✅ Warnings reset.")
        else:
            await message.reply("User has no warnings.")

    # Show warnings
    @app.on_message(filters.command("warns") & filters.group)
    @admin_only
    async def show_warns(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to check their warnings.")
            return

        user_id = str(message.reply_to_message.from_user.id)
        chat_id = str(message.chat.id)
        warnings = load_warnings()

        count = warnings.get(chat_id, {}).get(user_id, 0)
        await message.reply(f"⚠️ {message.reply_to_message.from_user.mention} has {count} warning(s).")

    # Mute
    @app.on_message(filters.command("mute") & filters.group)
    @admin_only
    async def mute_user(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to mute them.")
            return

        args = message.text.split()
        duration = int(args[1]) if len(args) > 1 and args[1].isdigit() else 0
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id

        await mute(client, chat_id, user_id, duration, message)

    # Unmute
    @app.on_message(filters.command("unmute") & filters.group)
    @admin_only
    async def unmute_user(client, message: Message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to unmute them.")
            return

        try:
            await client.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                )
            )
            await message.reply("✅ User has been unmuted.")
        except Exception as e:
            await message.reply(f"Failed to unmute: <code>{e}</code>")

# Utility mute function
async def mute(client, chat_id, user_id, duration, message):
    try:
        until_date = datetime.utcnow() + timedelta(minutes=duration) if duration > 0 else None
        await client.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(),  # Fully mute
            until_date=until_date
        )
        await message.reply(
            f"🔇 User has been muted {'for ' + str(duration) + ' minutes' if duration else 'indefinitely'}."
        )
    except Exception as e:
        await message.reply(f"Failed to mute: <code>{e}</code>")

