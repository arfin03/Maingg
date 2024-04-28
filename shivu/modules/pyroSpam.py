from pyrogram import  filters
from shivu import shivuu
import time

# Initialize Pyrogram client
app = shivuu

# Dictionary to keep track of last command usage timestamp for each user
last_command_usage = {}

# Command handler for /spam
@app.on_message(filters.command("spam") & filters.user(6783092268))
async def spam_command_handler(client, message):
    # Get the user ID
    user_id = message.from_user.id
    
    # Check if the user has used the command within the last minute
    if user_id in last_command_usage and time.time() - last_command_usage[user_id] < 60:
        # Send a message indicating the cooldown period
        await message.reply_text("You can only use this command once every minute.")
        return
    
    # Update the last command usage timestamp for the user
    last_command_usage[user_id] = time.time()
    
    # Send the sticker 10 times
    for _ in range(10):
        await message.reply_sticker("CAACAgQAAxkBASfxWWYtwIJQg63Tw82KmyZEAYQ_HYbFAALnDAAC1NZQU69xpuvJ3olDNAQ")
