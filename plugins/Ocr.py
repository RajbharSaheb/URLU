"""
 * @author        yasir <yasiramunandar@gmail.com>
 * @date          2022-12-01 09:12:27
 * @projectName   MissKatyPyro
 * Copyright @YasirPedia All rights reserved
"""


import os

from pyrogram import filters
from pyrogram.types import Message
from telegraph.aio import Telegraph

from pyrogram import Client as app
from functions.error import capture_err
from functions.https import fetch
from functions.https import rentry


@app.on_message(filters.command(["ocr"]))
@capture_err
async def ocr(_, ctx: Message, strings):
    reply = ctx.reply_to_message
    if (
        not reply
        or not reply.sticker
        and not reply.photo
        and (not reply.document or not reply.document.mime_type.startswith("image"))
    ):
        return await ctx.reply_msg(
            "Reply photo with /ocr command to scan text from images").format(cmd=ctx.command[0]), quote=True
        )
    msg = await ctx.reply_msg(strings("Scanning your images"), quote=True)
    try:
        file_path = await reply.download()
        if reply.sticker:
            file_path = await reply.download(
                f"ocr_{ctx.from_user.id if ctx.from_user else ctx.sender_chat.id}.jpg"
            )
        response = await Telegraph().upload_file(file_path)
        url = f"https://img.yasirweb.eu.org{response[0]['src']}"
        req = (
            await fetch.get(
                f"https://script.google.com/macros/s/AKfycbwURISN0wjazeJTMHTPAtxkrZTWTpsWIef5kxqVGoXqnrzdLdIQIfLO7jsR5OQ5GO16/exec?url={url}",
                follow_redirects=True,
            )
        ).json()
        await msg.edit_msg(strings("Hasil OCR:\n<code>{result}</code>",).format(result=req["text"]))
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        await msg.edit_msg(str(e))
        if os.path.exists(file_path):
            os.remove(file_path)
