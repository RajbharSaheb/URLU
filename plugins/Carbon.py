
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
    try:
        async with aiohttpsession.post(url, json={"code": code}) as resp:
            image = BytesIO(await resp.read())
    except Exception as e:
        return False, str(e)
    image.name = "carbon.png"
    return True, image


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
    success, carbon = await make_carbon(message.reply_to_message.text)
    if not success:
        return await m.edit(f"Error: {carbon}")
    await m.edit("Uploading..")
    try:
        await message.reply_photo(
            photo=carbon,
            caption="Coded By @Tamilan_BotsZ",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("SUPPORT US", url="https://t.me/mkn_bots_updates")]]),
        )
    except pyrogram.errors.exceptions.bad_request_400.ImageProcessFailed:
        return await m.edit("Telegram failed to process the image.")
    await m.delete()
    carbon.close()
