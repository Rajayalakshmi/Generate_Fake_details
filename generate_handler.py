import logging
import json
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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

country_flags = {
    'United States': '🇺🇸',
    'Turkey': '🇹🇷',
    'Egypt': '🇪🇬',
    'Bulgaria': '🇧🇬',
    'Belgium': '🇧🇪',
    'Saudi Arabia': '🇸🇦',
    'Jordan': '🇯🇴',
    'Bahrain': '🇧🇭',
    'Palestine': '🇵🇸',
    'United Arab Emirates': '🇦🇪'
}

def generate(update: Update, context: CallbackContext) -> None:
    valid_country_locale_map = context.bot_data.get('valid_country_locale_map', {})
    keyboard = []
    for country, locale in valid_country_locale_map.items():
        flag = country_flags.get(country, '')
        keyboard.append([InlineKeyboardButton(f"{flag} {country}", callback_data=country)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = update.message.reply_text('Select a Country:', reply_markup=reply_markup)

    save_message(context, 'Select a Country:')
    logger.debug("Sent country selection buttons")
