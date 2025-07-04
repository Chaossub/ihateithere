import asyncio
from pyrogram.types import ChatPermissions

async def mute(client, chat_id, user_id, duration=None):
    try:
        permissions = ChatPermissions()  # Empty = mute all
        await client.restrict_chat_member(chat_id, user_id, permissions)
        if duration:
            # Schedule an unmute in the background without blocking the main bot!
            asyncio.create_task(unmute_later(client, chat_id, user_id, duration))
        return True
    except Exception as e:
        print(f"❌ Mute error: {e}")
        return False

async def unmute_later(client, chat_id, user_id, duration):
    await asyncio.sleep(duration)
    await unmute(client, chat_id, user_id)

async def unmute(client, chat_id, user_id):
    try:
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_invite_users=True
        )
        await client.restrict_chat_member(chat_id, user_id, permissions)
        return True
    except Exception as e:
        print(f"❌ Unmute error: {e}")
        return False
