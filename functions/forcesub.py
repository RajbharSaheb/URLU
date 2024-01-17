import asyncio
from plugins.config import Config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

async def handle_force_subscribe(Client, message):
    try:
        invite_link = await Client.create_chat_invite_link(int(Config.UPDATES_CHANNEL), message.chat.id)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return 400
    try:
        user = await Client.get_chat_member(int(Config.UPDATES_CHANNEL), message.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry Sir, You are Banned. Contact My [Support Group](https://t.me/shado_hackers).",
                parse_mode="markdown",
                disable_web_page_preview=True,
                reply_to_message_id=message.id,
            )
            return 400
    except UserNotParticipant:
        await Client.send_message(
            chat_id=message.from_user.id,
            text="Please Join My Update Channel To Use Me",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("✴️ Join My Update Channel ✴️", url=invite_link.invite_link)
                    ]
                ]
            ),
            parse_mode="markdown",
            reply_to_message_id=message.id,
        )
        return 400
    except Exception:
        await Client.send_message(
            chat_id=message.from_user.id,
            text="Something Went Wrong. Contact My [Support Group](https://t.me/shado_hackers).",
            parse_mode="markdown",
            disable_web_page_preview=True,
           reply_to_message_id=message.id,
        )
        return 400
