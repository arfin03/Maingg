from pyrogram import  filters
from shivu import shivuu
import time
import random

# Initialize Pyrogram client
app = shivuu

# Dictionary to keep track of last command usage timestamp for each user
last_command_usage = {}


# List of sticker IDs (SPAM)
SPAM = [
    "CAACAgUAAxkBASf7S2Yt5RbDP7g4UePZDLIuexoWUcbKAALoDwACgNPxV8N-Ljw5GKpdNAQ",  # Sticker 1
    "CAACAgUAAxkBASf7TmYt5RgJeimG3b6OOx6-J3zQ85gtAAIUEAACQxnxV4uDU1R1x1VyNAQ",  # Sticker 2
    "CAACAgUAAxkBASf7T2Yt5RnZqytmLp4VhJZm53ffQwABEgAC9xAAAgmZ6FdfRsy2IIRQWDQE",  # Sticker 3
    "CAACAgUAAxkBASf7VGYt5SB3_gHYEnc7mKkF7T1xvDS8AAKSDQACziTwV1Xq7X-y6a6rNAQ",  # Sticker 4
    "CAACAgUAAxkBASf7VWYt5SCrQzheuicw26ZiL0d6ErnvAAMNAAKC3PBXk6uoSW_ey9Q0BA",  # Sticker 5
    # Add more sticker IDs here as needed
]

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
        await message.reply_sticker(random.choice(SPAM))
