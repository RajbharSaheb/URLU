import pyrogram
from pyrogram import Client, filters
import aiohttp

# Create a Pyrogram client instance
#client = Client("my_bard_client")

# Define the command handler for "/bard" command
@Client.on_message(filters.command("bard"))
async def bard(client, message):
    # Extract the user's query from the message
    query = None
    text_split = message.text.split(" ", 1)
    if len(text_split) > 1:
        query = text_split[1]

    # Construct the Bard API request URL
    api_url = f"https://api.safone.dev/bard?{query}"

    # Send a GET request to the Bard API
    async def get_data():
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                data = await response.json()
                return data

    # Call the async function using the await keyword
    data = await get_data()

    # Check if the response is successful
    if data["status"] == "success":
        # Extract the Bard response from the JSON data
        bard_response = data["response"]

        # Send the Bard response back to the user
        await message.reply_text(bard_response)
    else:
        # Handle the error
        await message.reply_text("Sorry, something went wrong. Please try again.")

# Start the Pyrogram client
#client.run()
