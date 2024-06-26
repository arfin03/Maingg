"""import os
import random
import html

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
import redis

from shivu import shivuu
from shivu import (application, PHOTO_URL, OWNER_ID,
                    user_collection, top_global_groups_collection, top_global_groups_collection, 
                    group_user_totals_collection)

from shivu import sudo_users as SUDO_USERS 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import *

# Redis connection setup
r = redis.Redis(
    host='redis-13192.c282.east-us-mz.azure.cloud.redislabs.com',
    port=13192,
    password='wKgGC52NC9NRhic36fDIvWh76dngPvP9')

async def tops(update: Update, context: CallbackContext) -> None:
    try:
        # Fetch all keys matching the pattern "user:*" in Redis
        user_keys = r.keys("user:*")

        # Initialize a dictionary to store user IDs and their charm counts
        user_charms = {}

        for key in user_keys:
            user_id = key.decode('utf-8').split(":")[-1]
            charms = r.hget(key, 'charm')
            if charms is not None:
                user_charms[user_id] = int(charms.decode('utf-8'))

        # Sort users based on charm counts
        sorted_users = sorted(user_charms.items(), key=lambda x: x[1], reverse=True)

        # Prepare leaderboard message
        leaderboard_message = "<b>Top Charms Leaderboard</b>\n\n"

        for i, (user_id, charms) in enumerate(sorted_users[:10], start=1):
            user_info_key = f'user:{user_id}'
            username = r.hget(user_info_key, 'username').decode('utf-8')
            first_name = r.hget(user_info_key, 'first_name').decode('utf-8')

            if len(first_name) > 10:
                first_name = first_name[:12] + '...'
            leaderboard_message += f'{i}. <a href="https://t.me/{username}">{first_name}</a> ➾ Charms: <code>{charms}</code>\n'

        photo_url = random.choice(PHOTO_URL)

        # Setup inline buttons
        keyboard = [[InlineKeyboardButton("🚮 Delete", callback_data='delete')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send message with inline buttons
        message = await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML', reply_markup=reply_markup)

        # Store the message ID for later deletion
        context.user_data['message_to_delete'] = message.message_id
    except Exception as e:
        print(f"Error in tops function: {e}")
        await update.message.reply_text('An error occurred while fetching the leaderboard.')

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'delete':
        # Delete the message using the stored message ID
        message_to_delete = context.user_data.get('message_to_delete')
        if message_to_delete:
            try:
                await context.bot.delete_message(chat_id=query.message.chat_id, message_id=message_to_delete)
            except Exception as e:
                print(f"Error deleting message: {e}")
        else:
            print("Message to delete not found.")

# Add the command and callback handlers
application.add_handler(CommandHandler('tops', tops, block=False))
application.add_handler(CallbackQueryHandler(button))
"""
