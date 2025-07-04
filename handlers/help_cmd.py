from pyrogram import filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("help"))
    async def help_handler(client, message: Message):
        text = """
<b>SuccuBot Commands</b>:

<b>Moderation (Admins/Owners only):</b>
/warn (reply) – Warn a user (3 warns = 5m mute, 6 warns = 10m mute)
/warns (reply) – See warning count
/resetwarns (reply) – Reset user warnings
/mute (reply) – Mute user (default: indefinite)
/unmute (reply) – Unmute user
/kick (reply) – Kick user from group
/ban (reply) – Ban user from group
/unban (reply) – Unban user
/flirtywarn (reply) – Flirty warning (does not mute)
/userinfo (reply) – View user info

<b>Federation (Admins/Owners only):</b>
/createfed [name]
/linkfed <fed_id>
/addfedadmin (reply)
/delfedadmin (reply)
/fedban (reply)
/fedunban (reply)
/fedcheck (reply)
/listfedgroups
/renamefed <name>
/delfed

<b>Fun & XP:</b>
/naughty – Check your Naughty XP
/leaderboard – Top 10 naughtiest users
/tease – Tease for XP
/spank – Spank for XP
/bite – Bite for XP

<b>Summon & Tracking:</b>
/track_all – Track all members (admin only)
/summonall – Mention all tracked users
/flirtysummonall – Flirty summon
/summon @username
/flirtysummon @username
/cancel

Welcome/goodbye, flirty messages, and more!
"""
        await message.reply(text)

