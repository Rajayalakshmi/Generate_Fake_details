import logging
import json
import urllib.parse
from telegram import Update
from telegram.ext import CallbackContext
from pymongo import MongoClient


logger = logging.getLogger(__name__)

# MongoDB setup
username = urllib.parse.quote_plus('jupyter123')
password = urllib.parse.quote_plus('Chinamade@123!')
uri = f'mongodb+srv://{username}:{password}@jupyter.n8v7v1s.mongodb.net/?retryWrites=true&w=majority&appName=Jupyter'
client = MongoClient(uri)
db = client['telegram_bot_db']
collection = db['chat_logs']

def save_message(context, message):
    if 'messages' not in context.chat_data:
        context.chat_data['messages'] = []
    context.chat_data['messages'].append(message)
    
    with open('chat_logs.json', 'w') as f:
        json.dump(context.chat_data['messages'], f)
    
    # Save to MongoDB
    collection.insert_one({'message': message})

def split_message(message, max_length=4096):
    return [message[i:i+max_length] for i in range(0, len(message), max_length)]

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    selected_country = query.data
    context.user_data['last_selected_country'] = selected_country
    details = context.bot_data['fake_details_map'][selected_country]
    max_key_length = max(len(key) for key in details.keys())
    details_message = f"\n**Fake details for {selected_country}:**\n\n" + "*-*"*10 + "\n"
    for key, value in details.items():
        if key == "ADDRESS":
            address_lines = value.split("\n")
            details_message += f"{key.ljust(max_key_length)}: {address_lines[0]}\n"
            for line in address_lines[1:]:
                details_message += f"{' ' * (max_key_length + 2)}{line}\n"
        else:
            details_message += f"{key.ljust(max_key_length)}: {value}\n"
    details_message += "\n" + "-"*20 + "\n"
    
    # Split and send the message if it's too long
    for msg in split_message(details_message):
        query.edit_message_text(text=msg, parse_mode='Markdown')

    save_message(context, details_message)
    logger.debug(f"Sent fake details for {selected_country}")
