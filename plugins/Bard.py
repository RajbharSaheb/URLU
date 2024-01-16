import asyncio
import pyrogram

from pyrogram import Client, filters

# Create a Pyrogram client instance
#client = Client("my_bard_client")

# Define the command handler
@client.on_message(filters.command("bard"))
async def bard_command(client, message):
    # Extract the user's query from the message
    query = message.text.split(" ", 1)[1]

    # Send the query to the Bard API
    async with client.session.get(f"https://api.safone.dev/bard?{query}") as response:
        # Parse the API response
        data = await response.json()

        # Extract the Bard response from the API response
        bard_response = data["response"]

    # Send the Bard response back to the user
    await message.reply_text(bard_response)

# Start the Pyrogram client
client.start()

# Keep the client running
client.idle()
