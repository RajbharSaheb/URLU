import pytz
import inspect
import logging
from datetime import datetime
import os
import math
import time
import shlex
import asyncio
from math import ceil
from pyrogram import Client
from traceback import format_exc
from typing import Tuple, Union
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import (
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message)
from plugins.translation import Translation

import mimetypes
import functools
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import sys
import traceback
from functools import wraps
from typing import Callable, Coroutine, Dict, List, Tuple, Union
import aiohttp
from PIL import Image
from pyrogram import Client as pbot
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Chat, Message, User

async def fetch_audio(client, message):
    time.time()
    if not message.reply_to_message:
        await message.reply("Reply To A Video / Audio.")
        return
    warner_stark = message.reply_to_message
    if warner_stark.audio is None and warner_stark.video is None:
        await message.reply("`Format Not Supported`")
        return
    if warner_stark.video:
        lel = await message.reply("`Video Detected, Converting To Audio !`")
        warner_bros = await message.reply_to_message.download()
        stark_cmd = f"ffmpeg -i {warner_bros} -map 0:a riya.mp3"
        await runcmd(stark_cmd)
        final_warner = "riya.mp3"
    elif warner_stark.audio:
        final_warner = await message.reply_to_message.download()
    await lel.delete()
    return final_warner

async def edit_or_reply(message, text, parse_mode="md"):
    if message.from_user.id:
        if message.reply_to_message:
            kk = message.reply_to_message.message_id
            return await message.reply_text(
                text, reply_to_message_id=kk, parse_mode=parse_mode
            )
        return await message.reply_text(text, parse_mode=parse_mode)
    return await message.edit(text, parse_mode=parse_mode)


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}]\n".format(
            ''.join(["✦" for i in range(math.floor(percentage / 10))]),
            ''.join(["✧" for i in range(10 - math.floor(percentage / 10))])
        )

        tmp = progress + Translation.PROGRESS.format(
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
              text="**{}**\n\n {}".format(
              ud_type,
              tmp
                ),
                parse_mode='markdown',
                reply_markup=InlineKeyboardMarkup(
                    [
                        [ 
                        InlineKeyboardButton('❌ Cancel', callback_data='close')
                       ]
                   ]
                 )
            )
        except:
            pass


def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
          ((str(hours) + "h, ") if hours else "") + \
          ((str(minutes) + "m, ") if minutes else "") + \
          ((str(seconds) + "s, ") if seconds else "") + \
          ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]
