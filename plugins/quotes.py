from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

# Sample Quotes Database (Replace with a real database later)
QUOTES = {
    "motivation": [
        "Success is not final, failure is not fatal: It is the courage to continue that counts.",
        "The only way to do great work is to love what you do.",
        "Your limitation—it’s only your imagination."
    ],
    "love": [
        "Love all, trust a few, do wrong to none.",
        "You are my heart, my life, my one and only thought.",
        "Love is not about how many days, months, or years you have been together. Love is about how much you love each other every single day."
    ],
    "inspiration": [
        "Believe you can and you're halfway there.",
        "You are never too old to set another goal or to dream a new dream.",
        "Do what you can, with what you have, where you are."
    ],
}

# Function to send category buttons
@Client.on_message(filters.command("quote") & filters.group)
async def send_quote_buttons(client, message):
    # Check if the user is an admin
    chat_id = message.chat.id
    user_id = message.from_user.id
    member = await client.get_chat_member(chat_id, user_id)
    
    if member.status not in ["administrator", "creator"]:
        await message.reply_text("🚫 You must be an admin to use this command.")
        return

    # Create category buttons
    buttons = [
        [InlineKeyboardButton("💪 Motivation", callback_data="quote_motivation")],
        [InlineKeyboardButton("❤️ Love", callback_data="quote_love")],
        [InlineKeyboardButton("🌟 Inspiration", callback_data="quote_inspiration")]
    ]

    await message.reply_text(
        "📌 Choose a category to get a quote:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Function to send quotes when a button is pressed
@Client.on_callback_query(filters.regex(r"^quote_"))
async def send_quote(client, callback_query):
    category = callback_query.data.split("_")[1]  # Extract category from callback data
    quote = random.choice(QUOTES[category])  # Pick a random quote

    await callback_query.message.reply_text(f"📜 {quote}")

    # Answer the callback query to remove "loading" state
    await callback_query.answer()
