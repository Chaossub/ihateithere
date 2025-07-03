from pyrogram.enums import ChatMemberStatus
from config import SUPERUSERS
from pyrogram.types import Message
from functools import wraps

async def is_admin_or_owner(client, chat_id, user_id):
    # Superuser bypass
    if user_id in SUPERUSERS:
        return True
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]

def admin_only(func):
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        if not await is_admin_or_owner(client, message.chat.id, message.from_user.id):
            await message.reply("This command is for admins or the group owner only.")
            return
        return await func(client, message, *args, **kwargs)
    return wrapper
