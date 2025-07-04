from pyrogram import filters
from pyrogram.types import Message
from config import SUPERUSERS
from handlers.utils import (
    admin_only,
    mute,
    unmute,
    get_warns,
    add_warn,
    reset_warns,
    save_warns,
)

from datetime import datetime
from asyncio import sleep


def register(app):
    # /warn command
    @app.on_message(filters.command("warn") & filters.group)
    @admin_only
    async def warn_user(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("❌ Reply to a user's message to warn them.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        warns = add_warn(user_id, chat_id)
        await message.reply(f"⚠️ User has been warned. Total warns: {warns}")

        if warns == 3:
            await mute(client, chat_id, user_id, 5, message)
        elif warns == 6:
            await mute(client, chat_id, user_id, 10, message)

    # /resetwarns command
    @app.on_message(filters.command("resetwarns") & filters.group)
    @admin_only
    async def reset_warn_cmd(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("❌ Reply to a user's message to reset warnings.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        reset_warns(user_id, chat_id)
        await message.reply("✅ Warnings have been reset.")

    # /warns command
    @app.on_message(filters.command("warns") & filters.group)
    @admin_only
    async def view_warns(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("❌ Reply to a user's message to check warnings.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        warns = get_warns(user_id, chat_id)
        await message.reply(f"⚠️ This user has {warns} warning(s).")

    # /mute command
    @app.on_message(filters.command("mute") & filters.group)
    @admin_only
    async def mute_cmd(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("❌ Reply to a user's message to mute them.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        try:
            parts = message.text.split()
            duration = int(parts[1]) if len(parts) > 1 else None
        except:
            duration = None
        await mute(client, chat_id, user_id, duration, message)

    # /unmute command
    @app.on_message(filters.command("unmute") & filters.group)
    @admin_only
    async def unmute_cmd(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("❌ Reply to a user's message to unmute them.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        await unmute(client, chat_id, user_id, message)

