from pyrogram import filters as Filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import CallbackQuery
from html import escape
from shivu import shivuu
import redis

# Redis connection setup
r = redis.Redis(
    host='redis-13192.c282.east-us-mz.azure.cloud.redislabs.com',
    port=13192,
    password='wKgGC52NC9NRhic36fDIvWh76dngPvP9'
)

# Define harem mode mapping
harem_mode_mapping = {
    "common": "⚪ Common",
    "rare": "🟣 Rare",
    "legendary": "🟡 Legendary",
    "medium": "🟢 Medium",
    "exclusive": "💮 Exclusive",
    "special_edition": "🫧 Special Edition",
    "limited_edition": "🔮 Limited Edition",
    "celestial": "🎐 Celestial",
    "christmas": "🎄 Christmas",
    "valentine": "💘 Valentine",
    "x_valentine": "💋 [𝙓] 𝙑𝙚𝙧𝙨𝙚",
    "cosplay": "🎭 𝘾𝙊𝙎𝙋𝙇𝘼𝙔 [𝙇]",
    "18+": "🔞 NSFW"
}

# Set hmode command handler
@shivuu.on_message(Filters.command("hhmode"))
async def set_hmode_command_handler(client, message):
    user_id = message.from_user.id
    keyboard = [
        [InlineKeyboardButton("⌠⚪⌡ ", callback_data="common"),
         InlineKeyboardButton("⌠🟣⌡ ", callback_data="rare"),
         InlineKeyboardButton("⌠🟢⌡ ", callback_data="medium")],
        [InlineKeyboardButton("⌠🟡⌡ ", callback_data="legendary"),
         InlineKeyboardButton("⌠🎄⌡ ", callback_data="christmas"),
         InlineKeyboardButton("⌠💘⌡ ", callback_data="valentine")],
        [InlineKeyboardButton("⌠💮⌡ ", callback_data="exclusive"),
         InlineKeyboardButton("⌠🫧⌡ ", callback_data="special_edition"),
         InlineKeyboardButton("⌠🔮⌡ ", callback_data="limited_edition")],
        [InlineKeyboardButton("˹🎐˼ ", callback_data="celestial"),
         InlineKeyboardButton("💋 [𝙓] 𝙑𝙚𝙧𝙨𝙚", callback_data="x_valentine"),
         InlineKeyboardButton("🎭 𝘾𝙊𝙎𝙋𝙇𝘼𝙔 [𝙇]", callback_data="cosplay"),
         InlineKeyboardButton("🔞 NSFW", callback_data="18+")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = await message.reply_photo(
        photo="https://telegra.ph/file/d7b82b55e6bc6d6fcf58b.jpg",
        caption="Set your harem mode:",
        reply_markup=reply_markup,
    )

# Button callback handler
@shivuu.on_callback_query()
async def button_callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data

    # Set hmode in Redis
    r.hset(f"{user_id}hmode", "rarity", data)
    try:
        await callback_query.answer(text=f"You set your harem mode to {harem_mode_mapping.get(data)}")
        await callback_query.edit_message_caption(f"You set your harem mode to {harem_mode_mapping.get(data)}")
    except Exception as e:
        print(e)￼Enter
