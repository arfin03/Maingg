from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from shivu import user_collection, shivuu

pending_trades = {}


@shivuu.on_message(filters.command("trade"))
async def trade(client, message):
    sender_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply_text("You need to reply to a user's message to trade a character!")
        return

    receiver_id = message.reply_to_message.from_user.id

    if sender_id == receiver_id:
        await message.reply_text("You can't trade a character with yourself!")
        return

    if len(message.command) != 3:
        await message.reply_text("You need to provide two character IDs!")
        return

    sender_character_id, receiver_character_id = message.command[1], message.command[2]

    sender = await user_collection.find_one({'id': sender_id})
    receiver = await user_collection.find_one({'id': receiver_id})

    sender_character = next((character for character in sender['characters'] if character['id'] == sender_character_id), None)
    receiver_character = next((character for character in receiver['characters'] if character['id'] == receiver_character_id), None)

    if not sender_character:
        await message.reply_text("You don't have the character you're trying to trade!")
        return

    if not receiver_character:
        await message.reply_text("The other user doesn't have the character they're trying to trade!")
        return






    if len(message.command) != 3:
        await message.reply_text("/trade [Your Character ID] [Other User Character ID]!")
        return

    sender_character_id, receiver_character_id = message.command[1], message.command[2]

    
    pending_trades[(sender_id, receiver_id)] = (sender_character_id, receiver_character_id)

    
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Confirm Trade", callback_data="confirm_trade")],
            [InlineKeyboardButton("Cancel Trade", callback_data="cancel_trade")]
        ]
    )

    await message.reply_text(f"{message.reply_to_message.from_user.mention}, do you accept this trade?", reply_markup=keyboard)


@shivuu.on_callback_query(filters.create(lambda _, __, query: query.data in ["confirm_trade", "cancel_trade"]))
async def on_callback_query(client, callback_query):
    receiver_id = callback_query.from_user.id

    
    for (sender_id, _receiver_id), (sender_character_id, receiver_character_id) in pending_trades.items():
        if _receiver_id == receiver_id:
            break
    else:
        await callback_query.answer("This is not for you!", show_alert=True)
        return

    if callback_query.data == "confirm_trade":
        
        sender = await user_collection.find_one({'id': sender_id})
        receiver = await user_collection.find_one({'id': receiver_id})

        sender_character = next((character for character in sender['characters'] if character['id'] == sender_character_id), None)
        receiver_character = next((character for character in receiver['characters'] if character['id'] == receiver_character_id), None)

        
        
        sender['characters'].remove(sender_character)
        receiver['characters'].remove(receiver_character)

        
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})
        await user_collection.update_one({'id': receiver_id}, {'$set': {'characters': receiver['characters']}})

        
        sender['characters'].append(receiver_character)
        receiver['characters'].append(sender_character)

        
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})
        await user_collection.update_one({'id': receiver_id}, {'$set': {'characters': receiver['characters']}})

        
        del pending_trades[(sender_id, receiver_id)]

        await callback_query.message.edit_text(f"You have successfully traded your character with {callback_query.message.reply_to_message.from_user.mention}!")

    elif callback_query.data == "cancel_trade":
        
        del pending_trades[(sender_id, receiver_id)]

        await callback_query.message.edit_text("❌️ Sad Cancelled....")



@shivuu.on_message(filters.command("gift"))
async def gift(client, message):
    sender_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply_text("You need to reply to a user's message to gift a character!")
        return

    receiver_id = message.reply_to_message.from_user.id
    receiver_username = message.reply_to_message.from_user.username
    receiver_first_name = message.reply_to_message.from_user.first_name

    if sender_id == receiver_id:
        await message.reply_text("You can't gift a character to yourself!")
        return

    if len(message.command) < 2:
        await message.reply_text("You need to provide at least one character ID to gift!")
        return

    character_ids = message.command[1:]

    sender = await user_collection.find_one({'id': sender_id})

    characters_to_gift = []
    characters_not_found = []

    for character_id in character_ids:
        character = next((char for char in sender['characters'] if char['id'] == character_id), None)
        if character:
            characters_to_gift.append(character)
        else:
            characters_not_found.append(character_id)

    if characters_not_found:
        await message.reply_text(f"You don't have the following characters in your collection: {', '.join(characters_not_found)}")
        return

    pending_gifts[(sender_id, receiver_id)] = {
        'characters': characters_to_gift,
        'receiver_username': receiver_username,
        'receiver_first_name': receiver_first_name
    }

    gift_list = "\n".join([f"{index + 1}. ({char['id']}) - {char['name'].lower()}" for index, char in enumerate(characters_to_gift)])

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Confirm Gift", callback_data="confirm_gift")],
            [InlineKeyboardButton("Cancel Gift", callback_data="cancel_gift")]
        ]
    )

    await message.reply_text(f"Do you really want to gift the following characters to {message.reply_to_message.from_user.mention}?\n\n{gift_list}", reply_markup=keyboard)

@shivuu.on_callback_query(filters.create(lambda _, __, query: query.data in ["confirm_gift", "cancel_gift"]))
async def on_gift_callback(client, callback_query):
    sender_id = callback_query.from_user.id

    for (_sender_id, receiver_id), gift_info in pending_gifts.items():
        if _sender_id == sender_id:
            break
    else:
        await callback_query.answer("This is not for you!", show_alert=True)
        return

    if callback_query.data == "confirm_gift":
        sender = await user_collection.find_one({'id': sender_id})
        receiver_id = gift_info['receiver_id']

        characters_to_gift = gift_info['characters']

        for character in characters_to_gift:
            sender['characters'].remove(character)

        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})

        receiver = await user_collection.find_one({'id': receiver_id})

        if receiver:
            receiver['characters'].extend(characters_to_gift)
            await user_collection.update_one({'id': receiver_id}, {'$set': {'characters': receiver['characters']}})
        else:
            await user_collection.insert_one({
                'id': receiver_id,
                'username': gift_info['receiver_username'],
                'first_name': gift_info['receiver_first_name'],
                'characters': characters_to_gift,
            })

        del pending_gifts[(sender_id, receiver_id)]

        await callback_query.message.edit_text(f"You have successfully gifted your characters to {gift_info['receiver_first_name']}!")
    elif callback_query.data == "cancel_gift":
        del pending_gifts[(sender_id, receiver_id)]
        await callback_query.message.edit_text("The gift has been canceled.")
