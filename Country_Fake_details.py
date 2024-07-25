import logging
from dotenv import load_dotenv
import os
from faker import Faker
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
from start_handler import start
from generate_handler import generate
from regenerate_handler import regenerate, generate_fake_details
from history_handler import history
from button_click_handler import button_click

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Initialize Faker and prepare data
fake = Faker()
load_dotenv()
country_locale_map = {
    'United States': 'en_US',
    'Turkey': 'tr_TR',
    'Egypt': 'ar_EG',
    'Bulgaria': 'bg_BG',
    'Belgium': 'fr_BE',
    'Saudi Arabia': 'ar_SA',
    'Jordan': 'ar_JO',
    'Bahrain': 'ar_BH',
    'Palestine': 'ar_PS',
    'United Arab Emirates': 'ar_AE'
}

valid_country_locale_map = {}
fake_details_map = {}

for country, locale in country_locale_map.items():
    try:
        fake = Faker(locale)
        details = generate_fake_details(fake, locale)
        if all(value != "N/A" for value in details.values()):
            valid_country_locale_map[country] = locale
            fake_details_map[country] = details
    except AttributeError:
        logging.warning(f"Skipping invalid locale: {locale}")

# Store data in dispatcher.bot_data
def store_data(dispatcher):
    dispatcher.bot_data['valid_country_locale_map'] = valid_country_locale_map
    dispatcher.bot_data['fake_details_map'] = fake_details_map

def unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Invalid Input, Please contact @TheCodingWizard if you face any issues.")

def main():
    # Replace 'YOUR_TOKEN' with your bot's token
    token = os.getenv('TOKEN')
    try:
        updater = Updater(token, request_kwargs={'read_timeout': 10, 'connect_timeout': 10})
        dispatcher = updater.dispatcher

        # Store data in dispatcher.bot_data
        store_data(dispatcher)

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("generate", generate))
        dispatcher.add_handler(CommandHandler("regenerate", regenerate))
        dispatcher.add_handler(CommandHandler("history", history))
        dispatcher.add_handler(CallbackQueryHandler(button_click))
        dispatcher.add_handler(MessageHandler(Filters.command, unknown))

        # Start the Bot
        updater.start_polling()
        logger.info("Bot started successfully")

        # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
        updater.idle()
    except Exception as e:
        logger.error(f"Failed to start the bot: {e}")

if __name__ == '__main__':
    main()
