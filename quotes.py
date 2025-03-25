import json
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import API_ID, API_HASH, BOT_TOKEN, QUOTES_CHANNEL_ID

# Load Quotes from JSON
def load_quotes():
    with open("quotes.json", "r") as file:
        return json.load(file)

quotes_data = load_quotes()

# Create Bot Client
app = Client("quote_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Command to send quote category options
@app.on_message(filters.command("quote") & filters.chat(QUOTES_CHANNEL_ID))
async def quote_options(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📌 Motivation", callback_data="quote_Motivation")],
        [InlineKeyboardButton("❤️ Love", callback_data="quote_Love")],
        [InlineKeyboardButton("🌟 Inspiration", callback_data="quote_Inspiration")]
    ])
    await message.reply_text("💡 Choose a quote category:", reply_markup=keyboard)

# Handle button clicks and send a random quote
@app.on_callback_query(filters.regex("^quote_"))
async def send_quote(client, callback_query: CallbackQuery):
    category = callback_query.data.split("_")[1]  # Extract category name
    if category in quotes_data:
        quote = random.choice(quotes_data[category])  # Pick random quote
        await callback_query.message.reply_text(f"💬 **{category} Quote:**\n\n_{quote}_")
    await callback_query.answer()  # Acknowledge button click

app.run()
