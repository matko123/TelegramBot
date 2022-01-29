
from telegram import ParseMode
from telegram.ext import CommandHandler, Defaults, Updater

from Alert import *

if __name__ == '__main__':
    updater = Updater(token=TELEGRAM_TOKEN, defaults=Defaults(parse_mode=ParseMode.HTML))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', startCommand)) # Accessed via /start
    dispatcher.add_handler(CommandHandler('alert', priceAlert)) # Accessed via /alert
    dispatcher.add_handler(CommandHandler('alert_looper', priceAlertLooper)) # Accessed via /alert
    dispatcher.add_handler(CommandHandler('update', priceUpdater))

    updater.start_polling() # Start the bot

    updater.idle() # Wait for the script to be stopped, this will stop the bot as well






