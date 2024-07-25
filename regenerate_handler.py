import logging
import json
import urllib.parse
from telegram import Update
from telegram.ext import CallbackContext
from pymongo import MongoClient
from faker import Faker

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

def regenerate(update: Update, context: CallbackContext) -> None:
    selected_country = context.user_data.get('last_selected_country')
    if not selected_country:
        update.message.reply_text("No previous country selected. Use /generate to select a country first.")
        logger.debug("No previous country selected for regeneration.")
        return

    locale = context.bot_data['valid_country_locale_map'][selected_country]
    fake = Faker(locale)
    new_details = generate_fake_details(fake, locale)
    context.bot_data['fake_details_map'][selected_country] = new_details

    max_key_length = max(len(key) for key in new_details.keys())
    details_message = f"\n**Regenerated fake details for {selected_country}:**\n\n" + "*-*"*10 + "\n"
    for key, value in new_details.items():
        if key == "ADDRESS":
            address_lines = value.split("\n")
            details_message += f"{key.ljust(max_key_length)}: {address_lines[0]}\n"
            for line in address_lines[1:]:
                details_message += f"{' ' * (max_key_length + 2)}{line}\n"
        else:
            details_message += f"{key.ljust(max_key_length)}: {value}\n"
    details_message += "\n" + "-"*20 + "\n"

    update.message.reply_text(details_message, parse_mode='Markdown')

    save_message(context, details_message)
    logger.debug(f"Sent regenerated fake details for {selected_country}")

def generate_fake_details(fake, locale):
    details = {}
    try:
        details["FIRST_NAME"] = fake.first_name().capitalize()
    except AttributeError:
        details["FIRST_NAME"] = "N/A"

    try:
        details["LAST_NAME"] = fake.last_name().capitalize()
    except AttributeError:
        details["LAST_NAME"] = "N/A"

    try:
        details["FULL_NAME"] = fake.name().title()
    except AttributeError:
        details["FULL_NAME"] = "N/A"

    try:
        details["ADDRESS"] = fake.address().title()
    except AttributeError:
        details["ADDRESS"] = "N/A"

    try:
        if hasattr(fake, 'postalcode'):
            details["ZIP_CODE"] = fake.postalcode()
        elif hasattr(fake, 'zipcode'):
            details["ZIP_CODE"] = fake.zipcode()
        else:
            details["ZIP_CODE"] = "N/A"
    except AttributeError:
        details["ZIP_CODE"] = "N/A"

    try:
        details["CITY"] = fake.city().capitalize()
    except AttributeError:
        details["CITY"] = "N/A"

    try:
        details["STATE"] = fake.state().capitalize() if hasattr(fake, 'state') else "N/A"
    except AttributeError:
        details["STATE"] = "N/A"

    return details
