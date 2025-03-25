# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import sys
import asyncio 
from database import Db, db
from config import Config, temp
from script import Script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument, CallbackQuery
import psutil
import time as time
from os import environ, execle, system
import json
import random
import time
from pyrogram import Client, filters, idle

START_TIME = time.time()

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

main_buttons = [[
    InlineKeyboardButton('❣️ ᴅᴇᴠᴇʟᴏᴘᴇʀ ❣️', url='https://t.me/kingvj01')
],[
    InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/vj_bot_disscussion'),
    InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/vj_botz')
],[
    InlineKeyboardButton('💝 sᴜʙsᴄʀɪʙᴇ ᴍʏ ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ', url='https://youtube.com/@Tech_VJ')
],[
    InlineKeyboardButton('👨‍💻 ʜᴇʟᴘ', callback_data='help'),
    InlineKeyboardButton('💁 ᴀʙᴏᴜᴛ', callback_data='about')
],[
    InlineKeyboardButton('⚙ sᴇᴛᴛɪɴɢs', callback_data='settings#main')
]]

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
    reply_markup = InlineKeyboardMarkup(main_buttons)
    await client.send_message(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text=Script.START_TXT.format(message.from_user.first_name))

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.private & filters.command(['restart']) & filters.user(Config.BOT_OWNER))
async def restart(client, message):
    msg = await message.reply_text(text="<i>Trying to restarting.....</i>")
    await asyncio.sleep(5)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
    execle(sys.executable, sys.executable, "main.py", environ)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^help'))
async def helpcb(bot, query):
    buttons = [[
        InlineKeyboardButton('🤔 ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ❓', callback_data='how_to_use')
    ],[
        InlineKeyboardButton('Aʙᴏᴜᴛ ✨️', callback_data='about'),
        InlineKeyboardButton('⚙ Sᴇᴛᴛɪɴɢs', callback_data='settings#main')
    ],[
        InlineKeyboardButton('• back', callback_data='back')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(text=Script.HELP_TXT, reply_markup=reply_markup)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def how_to_use(bot, query):
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=Script.HOW_USE_TXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^back'))
async def back(bot, query):
    reply_markup = InlineKeyboardMarkup(main_buttons)
    await query.message.edit_text(
       reply_markup=reply_markup,
       text=Script.START_TXT.format(query.from_user.first_name))

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query):
    buttons = [[
         InlineKeyboardButton('• back', callback_data='help'),
         InlineKeyboardButton('Stats ✨️', callback_data='status')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=Script.ABOUT_TXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^status'))
async def status(bot, query):
    users_count, bots_count = await db.total_users_bots_count()
    forwardings = await db.forwad_count()
    upt = await get_bot_uptime(START_TIME)
    buttons = [[
        InlineKeyboardButton('• back', callback_data='help'),
        InlineKeyboardButton('System Stats ✨️', callback_data='systm_sts'),
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=Script.STATUS_TXT.format(upt, users_count, bots_count, forwardings),
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^systm_sts'))
async def sys_status(bot, query):
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    disk_usage = psutil.disk_usage('/')
    total_space = disk_usage.total / (1024**3)  # Convert to GB
    used_space = disk_usage.used / (1024**3)    # Convert to GB
    free_space = disk_usage.free / (1024**3)
    text = f"""
╔════❰ sᴇʀᴠᴇʀ sᴛᴀᴛs  ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ <b>ᴛᴏᴛᴀʟ ᴅɪsᴋ sᴘᴀᴄᴇ</b>: <code>{total_space:.2f} GB</code>
║┣⪼ <b>ᴜsᴇᴅ</b>: <code>{used_space:.2f} GB</code>
║┣⪼ <b>ꜰʀᴇᴇ</b>: <code>{free_space:.2f} GB</code>
║┣⪼ <b>ᴄᴘᴜ</b>: <code>{cpu}%</code>
║┣⪼ <b>ʀᴀᴍ</b>: <code>{ram}%</code>
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪
"""
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def get_bot_uptime(start_time):
    # Calculate the uptime in seconds
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_weeks = uptime_days // 7
    uptime_string = ""
    if uptime_hours != 0:
        uptime_string += f" {uptime_hours % 24}H"
    if uptime_minutes != 0:
        uptime_string += f" {uptime_minutes % 60}M"
    uptime_string += f" {uptime_seconds % 60} Sec"
    return uptime_string   


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

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
