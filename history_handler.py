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

def history(update: Update, context: CallbackContext) -> None:
    history_limit = int(context.args[0]) if context.args else None
    try:
        with open('chat_logs.json', 'r') as f:
            messages = json.load(f)
    except FileNotFoundError:
        messages = context.chat_data.get('messages', [])
    
    # Load messages from MongoDB if local file not found or empty
    if not messages:
        messages = [doc['message'] for doc in collection.find()]

    if history_limit:
        messages = messages[-history_limit:]

    if not messages or all(not message.strip() for message in messages):
        update.message.reply_text("No history available.")
        logger.debug("No history available to show.")
        return

    history_message = "\n".join(message for message in messages if message.strip())
    
    # Split and send the message if it's too long
    for msg in split_message(history_message):
        update.message.reply_text(msg)

    # Export to HTML
    with open("history.html", "w") as f:
        f.write(f"<html><body><pre>{history_message}</pre></body></html>")

    update.message.reply_text("Chat history exported to history.html")
    logger.debug("Chat history exported to history.html")
