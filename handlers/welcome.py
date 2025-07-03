import random
from pyrogram import filters
from pyrogram.types import Message

def register(app):
    # Welcome message
    @app.on_message(filters.new_chat_members)
    async def welcome_handler(client, message: Message):
        new_members = message.new_chat_members
        for member in new_members:
            responses = [
                f"Welcome to the den of temptation, {member.mention} 😈",
                f"Hey {member.mention}, ready for some mischief?",
                f"{member.mention} just joined! Let the fun begin.",
                f"Welcome {member.mention}! Try not to get too naughty...",
                f"{member.mention}, you’re in for a wild ride!",
                f"Temptation awaits, {member.mention}…",
                f"{member.mention}, welcome to the club where the rules are always bent.",
                f"New arrival: {member.mention}. Hope you can handle us!",
                f"Watch out, {member.mention}—this group bites back!",
                f"{member.mention} has entered Succubus Sanctuary. Play nice (or don’t)."
            ]
            await message.reply(random.choice(responses))

    # Goodbye message
    @app.on_message(filters.left_chat_member)
    async def goodbye_handler(client, message: Message):
        member = message.left_chat_member
        responses = [
            f"Bye bye, {member.mention}! Come back if you crave more fun…",
            f"{member.mention} couldn’t handle the heat 😏",
            f"So long, {member.mention}! The temptation was too strong?",
            f"{member.mention} has left the party. We’ll miss your mischief!",
            f"Another soul lost: {member.mention}. Don’t stay away too long.",
            f"Farewell {member.mention}—your spot on the naughty list is waiting.",
            f"{member.mention} slipped away… but we always remember our naughtiest members.",
            f"Goodbye, {member.mention}! Hope you return when you’re ready for more trouble.",
            f"{member.mention} has left. The group just got less spicy.",
            f"{member.mention}, gone but never forgotten!"
        ]
        await message.reply(random.choice(responses))
