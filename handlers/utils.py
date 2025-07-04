from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatPermissions
from datetime import datetime, timedelta
import json

def get_warns(data, chat_id, user_id):
    return data.get(chat_id, {}).get(user_id, 0)

def add_warn(data, chat_id, user_id):
    if chat_id not in data:
        data[chat_id] = {}
    data[chat_id][user_id] = data[chat_id].get(user_id, 0) + 1
    return data[chat_id][user_id]

def reset_warns(data, chat_id, user_id):
    if chat_id in data and user_id in data[chat_id]:
        data[chat_id][user_id] = 0

def save_warns(data):
    with open("data/warnings.json", "w") as f:
        json.dump(data, f, indent=2)

def is_admin_or_owner(member):
    return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]

def admin_only(func):
    async def wrapper(client, message):
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if is_admin_or_owner(user):
            return await func(client, message)
        else:
            await message.reply("❌ You must be an admin to use this command.")
    return wrapper

async def mute(client, chat_id, user_id, duration, message):
    try:
        until_date = int((datetime.utcnow() + timedelta(minutes=duration)).timestamp()) if duration else None
        await client.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(),
            until_date=until_date
        )
        await message.reply(f"🔇 User muted {'for ' + str(duration) + ' minutes' if duration else 'indefinitely'}.")
    except Exception as e:
        await message.reply(f"Failed to mute: <code>{e}</code>")

async def unmute(client, chat_id, user_id, message):
    try:
        await client.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.reply("🔊 User has been unmuted.")
    except Exception as e:
        await message.reply(f"Failed to unmute: <code>{e}</code>")
