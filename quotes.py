import json
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import API_ID, API_HASH, BOT_TOKEN

# Load Quotes from JSON
def load_quotes():
    with open("quotes.json", "r") as file:
        return json.load(file)

quotes_data = load_quotes()

# Create Bot Client
app = Client("quote_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to Check if User is an Admin
async def is_admin(client, chat_id, user_id):
    chat_member = await client.get_chat_member(chat_id, user_id)
    return chat_member.status in ["administrator", "creator"]

# Command to send quote category buttons (Only for Admins)
@app.on_message(filters.command("quote") & filters.group)
async def quote_options(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        return await message.reply_text("🚫 You must be an admin to use this command.")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📌 Motivation", callback_data=f"quote_Motivation_{chat_id}")],
        [InlineKeyboardButton("❤️ Love", callback_data=f"quote_Love_{chat_id}")],
        [InlineKeyboardButton("🌟 Inspiration", callback_data=f"quote_Inspiration_{chat_id}")]
    ])
    await message.reply_text("💡 **Choose a quote category:**", reply_markup=keyboard)

# Handle button clicks and send a quote in the same channel
@app.on_callback_query(filters.regex("^quote_"))
async def send_quote(client, callback_query: CallbackQuery):
    _, category, chat_id = callback_query.data.split("_")  # Extract category and chat ID
    chat_id = int(chat_id)  # Convert chat_id back to integer

    if category in quotes_data:
        quote = random.choice(quotes_data[category])  # Pick random quote
        await client.send_message(chat_id, f"💬 **{category} Quote:**\n\n_{quote}_")

    await callback_query.answer()  # Acknowledge button click

app.run()
