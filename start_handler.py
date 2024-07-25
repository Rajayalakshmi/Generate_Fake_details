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

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    username = user.username if user.username else "None"
    user_id = user.id
    first_name = user.first_name if user.first_name else "None"
    last_name = user.last_name if user.last_name else "None"

    welcome_message = (
        f"Hi! I'm the Faker Bot 🤖\n\n"
        f"Hi {username},\n"
        f"**User ID:** {user_id}\n"
        f"**First Name:** {first_name}\n"
        f"**Last Name:** {last_name}\n\n"
        "This bot can generate fake details for various countries.\n"
        "Use these details for testing, development, or any fun purposes!\n\n"
        "Commands:\n"
        "⚪ /generate – Generate fake details\n"
        "⚪ /regenerate – Regenerate details for the last selected country\n"
        "⚪ /history – Show command history\n\n"
        "Type /generate to start generating fake details."
    )

    update.message.reply_text(welcome_message, parse_mode='Markdown')

    save_message(context, welcome_message)
    logger.debug(f"Sent welcome message to {username}")
