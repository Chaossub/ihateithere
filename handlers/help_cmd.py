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
/mute [seconds] (reply) – Mute user (with optional timer, default indefinite)
/unmute (reply) – Unmute user
/kick (reply) – Kick user from group
/ban (reply) – Ban user from group
/unban (reply) – Unban user
/flirtywarn (reply) – Send a flirty warning (does not count toward mute)
/userinfo (reply) – View user info

<b>Federation (Admins/Owners only):</b>
/createfed [name] – Create federation
/linkfed &lt;fed_id&gt; – Link group to a federation
/addfedadmin (reply) – Add federation admin
/delfedadmin (reply) – Remove federation admin
/fedban (reply) – Federation ban user
/fedunban (reply) – Federation unban user
/fedcheck (reply) – Check if federated banned
/listfedgroups – List groups in federation
/renamefed &lt;name&gt; – Rename federation
/delfed – Delete federation

<b>Fun & XP:</b>
/naughty – Check your Naughty XP
/leaderboard – Top 10 naughtiest users
/tease – Tease for XP
/spank – Spank for XP
/bite – Bite for XP

<b>Summon & Tracking:</b>
/track_all – Track all group members for summons (admin only)
/summonall – Mention all tracked users
/flirtysummonall – Flirty version of summon all
/summon @username – Summon a specific user
/flirtysummon @username – Flirty summon for a user
/cancel – Cancel the current command (if needed)

<b>Welcome/Goodbye:</b>
– Flirty, random welcomes and goodbyes for joins/leaves!

All admin-only commands are protected for group owner/admins (or you if you’re a superuser).

Enjoy SuccuBot! 😈
"""
        await message.reply(text)
