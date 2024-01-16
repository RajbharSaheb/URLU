
import pyrogram
from pyrogram import filters, types
from datetime import datetime, timedelta
import calendar
from pyrogram import Client 

# Initialize the bot client
#bot = pyrogram.Client("calendar_bot", api_id=123456, api_hash="0123456789abcdef")

# Define a command handler for "/calendar"
@Client.on_message(filters.command("calendar"))
async def calendar_handler(client: pyrogram.Client, message: pyrogram.types.Message):
    # Get the current month and year
    now = datetime.now()
    month = now.month
    year = now.year

    # Generate the calendar for the current month
    cal = calendar.TextCalendar()
    calendar_text = cal.formatmonth(year, month)

    # Send the calendar to the user
    await message.reply_text(calendar_text)

# Define a command handler for "/next"
@Client.on_message(filters.command("next"))
async def next_handler(client: pyrogram.Client, message: pyrogram.types.Message):
    # Get the current month and year
    now = datetime.now()
    month = now.month
    year = now.year

    # Get the next month
    next_month = month + 1
    if next_month > 12:
        next_month = 1
        year += 1

    # Generate the calendar for the next month
    cal = calendar.TextCalendar()
    calendar_text = cal.formatmonth(year, next_month)

    # Send the calendar to the user
    await message.reply_text(calendar_text)

# Define a command handler for "/previous"
@Client.on_message(filters.command("previous"))
async def previous_handler(client: pyrogram.Client, message: pyrogram.types.Message):
    # Get the current month and year
    now = datetime.now()
    month = now.month
    year = now.year

    # Get the previous month
    previous_month = month - 1
    if previous_month < 1:
        previous_month = 12
        year -= 1

    # Generate the calendar for the previous month
    cal = calendar.TextCalendar()
    calendar_text = cal.formatmonth(year, previous_month)

    # Send the calendar to the user
    await message.reply_text(calendar_text)
