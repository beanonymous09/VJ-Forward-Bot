import json
import random
import asyncio
from datetime import datetime, time
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import API_ID, API_HASH, BOT_TOKEN

# Load Quotes from JSON
def load_quotes():
    with open("quotes.json", "r") as file:
        return json.load(file)

quotes_data = load_quotes()

# Load Scheduled Jobs
def load_scheduled_jobs():
    try:
        with open("scheduled_quotes.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_scheduled_jobs(jobs):
    with open("scheduled_quotes.json", "w") as file:
        json.dump(jobs, file, indent=4)

scheduled_jobs = load_scheduled_jobs()

# Create Bot Client
app = Client("quote_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to Check if User is an Admin
async def is_admin(client, chat_id, user_id):
    try:
        chat_member = await client.get_chat_member(chat_id, user_id)
        return chat_member.status in ["administrator", "creator"]
    except:
        return False

# Command to send quote category buttons with scheduling
@app.on_message(filters.command("quote") & filters.group)
async def quote_options(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        return await message.reply_text("🚫 Only admins can use this command.")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📌 Motivation", callback_data=f"quote_Motivation_{chat_id}")],
        [InlineKeyboardButton("❤️ Love", callback_data=f"quote_Love_{chat_id}")],
        [InlineKeyboardButton("🌟 Inspiration", callback_data=f"quote_Inspiration_{chat_id}")],
        [InlineKeyboardButton("🕒 Schedule a Quote", callback_data=f"schedule_{chat_id}")]
    ])
    await message.reply_text("💡 **Choose an option:**", reply_markup=keyboard)

# Handle button clicks and send a quote in the same channel
@app.on_callback_query(filters.regex("^quote_"))
async def send_quote(client, callback_query: CallbackQuery):
    _, category, chat_id = callback_query.data.split("_")
    chat_id = int(chat_id)

    if category in quotes_data:
        quote = random.choice(quotes_data[category])
        await client.send_message(chat_id, f"💬 **{category} Quote:**\n\n_{quote}_")

    await callback_query.answer()

# Handle Scheduling Request
@app.on_callback_query(filters.regex("^schedule_"))
async def schedule_quote(client, callback_query: CallbackQuery):
    chat_id = int(callback_query.data.split("_")[1])
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📌 Motivation", callback_data=f"set_schedule_Motivation_{chat_id}")],
        [InlineKeyboardButton("❤️ Love", callback_data=f"set_schedule_Love_{chat_id}")],
        [InlineKeyboardButton("🌟 Inspiration", callback_data=f"set_schedule_Inspiration_{chat_id}")]
    ])
    await callback_query.message.reply_text("📅 **Select a category to schedule:**", reply_markup=keyboard)
    await callback_query.answer()

# Step 2: Ask for Time Input After Category Selection
@app.on_callback_query(filters.regex("^set_schedule_"))
async def ask_schedule_time(client, callback_query: CallbackQuery):
    _, _, category, chat_id = callback_query.data.split("_")
    chat_id = int(chat_id)

    scheduled_jobs[str(chat_id)] = {"category": category}
    save_scheduled_jobs(scheduled_jobs)
    
    await callback_query.message.reply_text("🕒 **Send the time in HH:MM format (24-hour format).**\nExample: `15:30`")
    await callback_query.answer()

# Step 3: Store the Time and Schedule the Quote
@app.on_message(filters.text & filters.group)
async def set_scheduled_time(client, message):
    chat_id = str(message.chat.id)
    if chat_id not in scheduled_jobs:
        return
    
    try:
        schedule_time = datetime.strptime(message.text.strip(), "%H:%M").time()
        scheduled_jobs[chat_id]["time"] = schedule_time.strftime("%H:%M")
        save_scheduled_jobs(scheduled_jobs)
        await message.reply_text(f"✅ **Quote scheduled at {message.text.strip()} for {scheduled_jobs[chat_id]['category']} category!**")
    except ValueError:
        await message.reply_text("❌ Invalid format! Please send time in `HH:MM` (24-hour format).")

# Step 4: Background Task to Send Scheduled Quotes
async def scheduled_task():
    while True:
        now = datetime.now().strftime("%H:%M")
        for chat_id, details in scheduled_jobs.items():
            if details.get("time") == now:
                category = details["category"]
                quote = random.choice(quotes_data.get(category, ["No quotes available."]))
                await app.send_message(int(chat_id), f"⏰ **Scheduled {category} Quote:**\n\n_{quote}_")
        await asyncio.sleep(60)  # Check every minute

# Run the bot and background task
async def main():
    await app.start()
    asyncio.create_task(scheduled_task())  # Start scheduling in the background
    await idle()  # Keep the bot running

if __name__ == "__main__":
    asyncio.run(main())
