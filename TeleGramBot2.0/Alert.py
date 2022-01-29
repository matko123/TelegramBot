import numpy as np
from coinbase.wallet.client import Client

COINBASE_KEY = 'lZyb6kpfyLyRKG31'
COINBASE_SECRET = 'Nvn4oWqelwDdk46k4o6x96lUpmou5Tu6'
TELEGRAM_TOKEN = '5108384712:AAFwZz7hzeP1659GI1FddI84GFxbRAZkcvA'

coinbase_client = Client(COINBASE_KEY, COINBASE_SECRET)

from Callback import *

def startCommand(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='To je malo jace!')

def priceUpdater(update, context):

    if len(context.args) == 1:
        crypto = context.args[0].upper()

        response = f"⚠ the current price of {crypto} is {coinbase_client.get_spot_price(currency_pair=crypto + '-USD')['amount']} $"
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    else:
        response = '⚠️ Please provide only a crypto code ex. /update BTC'
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def priceAlert(update, context):

    if len(context.args) > 2:
        crypto = context.args[0].upper()
        sign = context.args[1]
        price = context.args[2]

        context.job_queue.run_repeating(priceAlertCallback, interval=15, first=15,
                                        context=[crypto, sign, price, update.message.chat_id])

        response = f"I will send you a message when the price of {crypto} reaches {price} $, \n"
        response += f"⚠ the current price of {crypto} is {coinbase_client.get_spot_price(currency_pair=crypto + '-USD')['amount']} $"
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    else:
        response = '⚠️ Please provide a crypto code and a price value, ex. /alert BTC < 20000 '
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def priceAlertLooper(update, context):

    if len(context.args) > 2:

        crypto = context.args[0].upper()
        sign = context.args[1]
        bottom_range = context.args[2]
        upper_range = context.args[3]
        distance = context.args[4]

        l = [i for i in np.arange(float(bottom_range), float(upper_range), float(distance))]

        for price in l:

            context.job_queue.run_repeating(priceAlertLooperCallback, interval=15, first=15,
                                            context=[crypto, price, sign, bottom_range, upper_range, distance,  update.message.chat_id])

            response = f"I will send you a message when the price of {crypto} reaches {price}$, \n"
            response += f"⚠ The current price of {crypto} is {coinbase_client.get_spot_price(currency_pair=crypto + '-USD')['amount']}$"
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    else:
        response = '⚠ Please provide bottom range, upper range and the step ex. /alert_looper BTC < 30000.0000  40000.0000 2000.0000'
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)