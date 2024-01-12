
from pyrogram import filters
from aiohttp import ClientSession
from pyrogram import Client as bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asyncio import gather
from datetime import datetime, timedelta
from io import BytesIO
from math import atan2, cos, radians, sin, sqrt

aiohttpsession = ClientSession()

async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiohttpsession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@bot.on_message(filters.command("carbon"))
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a text message to make carbon."
        )
    if not message.reply_to_message.text:
        return await message.reply_text(
            "Reply to a text message to make carbon."
        )
    user_id = message.from_user.id
    m = await message.reply_text("Processing...")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("Uploading..")
    await message.reply_photo(
        photo=carbon,
        caption="Coded By @shado_hackers",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("SUPPORT US", url="https://t.me/omg_info")]]),
    )
    await m.delete()
    carbon.close()
