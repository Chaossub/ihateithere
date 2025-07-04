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
            return await message.reply("Reply to a user to warn them.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        warns = add_warn(user_id)
        await message.reply(f"User has been warned. Total warnings: {warns}")
        if warns == 3:
            await mute(client, chat_id, user_id, duration_seconds=300)
            await message.reply("User has been muted for 5 minutes due to 3 warnings.")
        elif warns == 6:
            await mute(client, chat_id, user_id, duration_seconds=600)
            await message.reply("User has been muted for 10 minutes due to 6 warnings.")

    # /resetwarns command
    @app.on_message(filters.command("resetwarns") & filters.group)
    @admin_only
    async def reset_user_warns(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("Reply to a user to reset their warnings.")
        user_id = message.reply_to_message.from_user.id
        reset_warns(user_id)
        await message.reply("Warnings reset for this user.")

    # /warns command
    @app.on_message(filters.command("warns") & filters.group)
    @admin_only
    async def check_warns(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("Reply to a user to check their warnings.")
        user_id = message.reply_to_message.from_user.id
        warns = get_warns().get(str(user_id), 0)
        await message.reply(f"User has {warns} warning(s).")

    # /mute command
    @app.on_message(filters.command("mute") & filters.group)
    @admin_only
    async def mute_user(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("Reply to a user to mute them.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        if await mute(client, chat_id, user_id):
            await message.reply("User has been muted.")
        else:
            await message.reply("Failed to mute.")

    # /unmute command
    @app.on_message(filters.command("unmute") & filters.group)
    @admin_only
    async def unmute_user(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("Reply to a user to unmute them.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        if await unmute(client, chat_id, user_id):
            await message.reply("User has been unmuted.")
        else:
            await message.reply("Failed to unmute.")

