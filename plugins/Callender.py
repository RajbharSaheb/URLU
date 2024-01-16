import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Create a new Pyrogram client instance
#app = Client("calendar_bot")

# Start command handler
@Client.on_message(filters.command("Callender"))
def start_command(client, message):
    # Get current date and time
    current_date = datetime.datetime.now()
    
    # Generate calendar markup
    calendar_markup = generate_calendar_markup(current_date.year, current_date.month)
    
    # Send calendar to user
    message.reply_text("Here is the calendar:", reply_markup=calendar_markup)

# Callback data handler
@Client.on_callback_query()
def callback_handler(client, callback_query):
    # Get callback data from inline button
    callback_data = callback_query.data
    
    # Extract year, month, and day from callback data
    year, month, day = map(int, callback_data.split("_"))
    
    # Create a datetime object with the selected date
    selected_date = datetime.datetime(year, month, day)
    
    # Format the date to a readable string
    selected_date_string = selected_date.strftime("%Y-%m-%d")
    
    # Send the selected date to the user
    client.send_message(
        chat_id=callback_query.message.chat.id,
        text=f"You selected: {selected_date_string}"
    )

# Function to generate the calendar markup
def generate_calendar_markup(year, month):
    # Get calendar for the specified year and month
    calendar = calendar.monthcalendar(year, month)  # Moved this line up
    
    # Create a list to store calendar buttons
    buttons = []
    
    # Add previous and next month buttons
    buttons.append(InlineKeyboardButton("<", callback_data=f"{year}_{month-1}_0"))
    buttons.append(InlineKeyboardButton(">", callback_data=f"{year}_{month+1}_0"))
    
    # Add weekdays header row
    buttons_row = []
    for weekday in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        buttons_row.append(InlineKeyboardButton(weekday, callback_data="ignore"))
    buttons.append(buttons_row)
    
    # Add days rows
    for week in calendar:
        buttons_row = []
        for day in week:
            if day == 0:
                buttons_row.append(InlineKeyboardButton(" ", callback_data="ignore"))
            else:
                buttons_row.append(InlineKeyboardButton(str(day), callback_data=f"{year}_{month}_{day}"))
        buttons.append(buttons_row)
    
    return InlineKeyboardMarkup(buttons)

# Run the Pyrogram client
#app.run()
