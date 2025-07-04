import json
import os
from pyrogram.types import ChatPermissions
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid

from config import SUPERUSERS

WARNINGS_FILE = "data/warnings.json"

def load_warnings():
    if os.path.exists(WARNINGS_FILE):
        with open(WARNINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_warns(warns):
    with open(WARNINGS_FILE, "w") as f:
        json.dump(warns, f, indent=4)

def get_warns(chat_id, user_id):
    warns = load_warnings()
    return warns.get(str(chat_id), {}).get(str(user_id), 0)

def add_warn(chat_id, user_id):
    warns = load_warnings()
    chat_warns = warns.setdefault(str(chat_id), {})
    chat_warns[str(user_id)] = chat_warns.get(str(user_id), 0) + 1
    save_warns(warns)
    return chat_warns[str(user_id)]

def reset_warns(chat_id, user_id):
    warns = load_warnings()
    if str(chat_id) in warns and str(user_id) in warns[str(chat_id)]:
        warns[str(chat_id)][str(user_id)] = 0
        save_warns(warns)

def admin_only(func):
    async def wrapper(client, message):
        user_id = message.from_user.id
        chat_id = message.chat.id

        # Allow superusers
        if user_id in SUPERUSERS:
            return await func(client, message)

        member = await client.get_chat_member(chat_id, user_id)
        if member.status in ("administrator", "creator"):
            return await func(client, message)
        await message.reply("🚫 You need to be an admin to use this command.")
    return wrapper

async def is_admin_or_owner(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except:
        return False

async def mute(client, chat_id, user_id):
    try:
        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False
        )
        await client.restrict_chat_member(chat_id, user_id, permissions=permissions)
        return True
    except (ChatAdminRequired, UserAdminInvalid):
        return False

async def unmute(client, chat_id, user_id):
    try:
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        await client.restrict_chat_member(chat_id, user_id, permissions=permissions)
        return True
    except (ChatAdminRequired, UserAdminInvalid):
        return False

