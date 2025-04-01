import asyncio
import logging
import random
import json
from datetime import datetime
from config import Config
from pyrogram import Client, filters
from pyrogram.types import Message

# Loading quotes from quotes.json
def load_quotes():
    with open("quotes.json", "r") as file:
        data = json.load(file)
    return data

quotes_data = load_quotes()

# Function to pick a random quote from the loaded quotes
def get_random_quote():
    category = random.choice(list(quotes_data.keys()))  # Randomly pick a category
    quote = random.choice(quotes_data[category])  # Randomly pick a quote from the category
    return f"{category} Quote: {quote}"

# Async function to send quote at the top of every hour
async def send_hourly_quote(client: Client):
    while True:
        # Get current time
        now = datetime.now()
        
        if now.minute == 0:  # Check if it's the start of the hour
            # Send a random quote
            quote = get_random_quote()
            await client.send_message(Config.CHAT_ID, quote)
        
        # Wait for 60 seconds before checking again
        await asyncio.sleep(60)

# Setting up pyrogram client
app = Client(
    "VJ-Forward-Bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
)

@app.on_message(filters.command("ping"))
async def ping_pong(client: Client, message: Message):
    await message.reply_text("Pong!")

if __name__ == "__main__":
    # Run the hourly quote sender in the background
    app.loop.create_task(send_hourly_quote(app))
    
    # Start the bot
    app.run()
