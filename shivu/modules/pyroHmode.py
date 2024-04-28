"""from pyrogram import filters as Filters 
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from html import escape
from shivu import shivuu

# Store user's harem mode locally (in-memory dictionary for illustration)
user_harem_modes = {}

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
        [InlineKeyboardButton("⌠⚪⌡ Common", callback_data="common"),
         InlineKeyboardButton("⌠🟣⌡ Rare", callback_data="rare"),
         InlineKeyboardButton("⌠🟢⌡ Medium", callback_data="medium")],
        [InlineKeyboardButton("⌠🟡⌡ Legendary", callback_data="legendary"),
         InlineKeyboardButton("⌠🎄⌡ Christmas", callback_data="christmas"),
         InlineKeyboardButton("⌠💘⌡ Valentine", callback_data="valentine")],
        [InlineKeyboardButton("⌠💮⌡ Exclusive", callback_data="exclusive"),
         InlineKeyboardButton("⌠🫧⌡ Special Edition", callback_data="special_edition"),
         InlineKeyboardButton("⌠🔮⌡ Limited Edition", callback_data="limited_edition")],
        [InlineKeyboardButton("˹🎐˼ Celestial", callback_data="celestial"),
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

    # Store user's harem mode locally
    user_harem_modes[user_id] = data
    try:
        await callback_query.answer(text=f"You set your harem mode to {harem_mode_mapping.get(data)}")
    
    except Exception as e:
        print(e)"""
