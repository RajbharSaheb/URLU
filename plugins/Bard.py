import pyrogram

# Initialize the Pyrogram Client
#client = pyrogram.Client("my_session_name", api_id=1234567, api_hash="abcdefgh")

# Start the client
Client.start()

# Define the command handler
@Client.on_message(pyrogram.filters.command("bard"))
def bard_command(client, message):
    # Extract the message text
    message_text = message.text

    # Remove the command from the message text
    query = message_text.replace("/bard", "").strip()

    # Send the query to the Bard AI API
    response = requests.get("https://api.safone.dev/bard?{query}")

    # Parse the response
    response_json = response.json()
    output = response_json["response"]

    # Send the response to the user
    message.reply_text(output)

# Keep the client running
#client.idle()
