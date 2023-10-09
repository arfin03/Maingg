from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pymongo import MongoClient
import urllib.request

# Connect to MongoDB
client = MongoClient('mongodb+srv://shuyaaaaa12:NvpoBuRp7MVPcAYA@cluster0.q2yycqx.mongodb.net/')
db = client['Waifusss']
collection = db['anime_characters']

# List of sudo users
sudo_users = ['6404226395']

def upload(update: Update, context: CallbackContext) -> None:
    # Check if user is a sudo user
    if str(update.effective_user.id) not in sudo_users:
        update.message.reply_text('You do not have permission to use this command.')
        return

    try:
        # Extract arguments
        args = context.args
        if len(args) != 3:
            update.message.reply_text('Incorrect format. Please use: /upload img_url Character-Name Anime-Name')
            return

        # Replace '-' with ' ' in character name
        character_name = args[1].replace('-', ' ')

        # Check if image URL is valid
        try:
            urllib.request.urlopen(args[0])
        except:
            update.message.reply_text('Invalid image URL.')
            return

        # Generate ID
        id = str(collection.count_documents({}) + 1).zfill(4)

        # Insert new character
        character = {
            'img_url': args[0],
            'name': character_name,
            'anime': args[2],
            'id': id
        }
        collection.insert_one(character)
        
        update.message.reply_text('Successfully uploaded.')

        # Send message to channel
        context.bot.send_photo(
            chat_id='-1001865838715',
            photo=args[0],
            caption=f'<b>Character Name:</b> {character_name}\n<b>Anime Name:</b> {args[2]}\n<b>ID:</b> {id}\nAdded by <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
            parse_mode='HTML'
        )
    except Exception as e:
        update.message.reply_text('Unsuccessfully uploaded.')

def anime(update: Update, context: CallbackContext) -> None:
    try:
        # Get all unique anime names
        anime_names = collection.distinct('anime')

        # Send message with anime names
        update.message.reply_text('\n'.join(anime_names))
    except Exception as e:
        update.message.reply_text('Failed to fetch anime names.')

def delete(update: Update, context: CallbackContext) -> None:
    # Check if user is a sudo user
    if str(update.effective_user.id) not in sudo_users:
        update.message.reply_text('You do not have permission to use this command.')
        return

    try:
        # Extract arguments
        args = context.args
        if len(args) != 1:
            update.message.reply_text('Incorrect format. Please use: /delete ID')
            return

        # Delete character with given ID
        result = collection.delete_one({'id': args[0]})

        if result.deleted_count > 0:
            update.message.reply_text('Successfully deleted.')
        else:
            update.message.reply_text('No character found with given ID.')
    except Exception as e:
        update.message.reply_text('Failed to delete character.')

def total(update: Update, context: CallbackContext) -> None:
    try:
        # Extract arguments
        args = context.args
        if len(args) != 1:
            update.message.reply_text('Incorrect format. Please use: /total Anime-Name')
            return

        # Replace '-' with ' ' in anime name
        anime_name = args[0].replace('-', ' ')

        # Get all characters of the given anime
        characters = collection.find({'anime': anime_name})

        # Create a list of character names and IDs
        character_list = [f'Character Name: {character["name"]}\nID: {character["id"]}' for character in characters]

        # Send message with character names and IDs
        update.message.reply_text('\n\n'.join(character_list))
    except Exception as e:
        update.message.reply_text('Failed to fetch characters.')

# Counter for messages in each group
message_counters = {}

# Last sent character in each group
last_characters = {}

# Characters that have been sent in each group
sent_characters = {}

def message_counter(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    # Increment counter for this chat
    if chat_id not in message_counters:
        message_counters[chat_id] = 0
    message_counters[chat_id] += 1

    # Send image after every 20 messages
    if message_counters[chat_id] % 20 == 0:
        send_image(update, context)

def send_image(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    # Get all characters
    all_characters = list(collection.find({}))

    # Initialize sent characters list for this chat if it doesn't exist
    if chat_id not in sent_characters:
        sent_characters[chat_id] = []

    # Reset sent characters list if all characters have been sent
    if len(sent_characters[chat_id]) == len(all_characters):
        sent_characters[chat_id] = []

    # Select a random character that hasn't been sent yet
    character = random.choice([c for c in all_characters if c['id'] not in sent_characters[chat_id]])

    # Add character to sent characters list and set as last sent character
    sent_characters[chat_id].append(character['id'])
    last_characters[chat_id] = character

    # Send image with caption
    context.bot.send_photo(
        chat_id=chat_id,
        photo=character['img_url'],
        caption="Use /Guess Command And.. Guess This Character Name.."
    )

def guess(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    # Check if a character has been sent in this chat yet
    if chat_id not in last_characters:
        update.message.reply_text('No character has been sent yet.')
        return

    # Check if guess is correct
    guess = ' '.join(context.args).lower()
    if guess in last_characters[chat_id]['name'].lower():
        update.message.reply_text('Correct guess!')

        # Add character to user's DB (not implemented)
        # ...
    else:
        update.message.reply_text('Incorrect guess.')



def main() -> None:
    updater = Updater(token='6526883785:AAEAGc396CqAuokk5o237ZP4k6dIhB0d6_k')

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('upload', upload))
    dispatcher.add_handler(CommandHandler('anime', anime))
    dispatcher.add_handler(CommandHandler('delete', delete))
    dispatcher.add_handler(CommandHandler('total', total))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_counter))
    dispatcher.add_handler(CommandHandler('guess', guess))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()