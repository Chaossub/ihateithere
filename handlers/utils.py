from pyrogram.types import ChatPermissions
import asyncio

async def mute(client, chat_id, user_id, duration=None):
    try:
        # Restrict all permissions (mute)
        permissions = ChatPermissions()
        await client.restrict_chat_member(chat_id, user_id, permissions)

        # If a duration was given, schedule unmute
        if duration:
            await asyncio.sleep(duration)
            await unmute(client, chat_id, user_id)
        return True
    except Exception as e:
        print(f"❌ Mute error: {e}")
        return False

async def unmute(client, chat_id, user_id):
    try:
        # Restore standard chat permissions
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
