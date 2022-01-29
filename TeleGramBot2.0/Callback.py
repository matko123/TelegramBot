from coinbase.wallet.client import Client

COINBASE_KEY = 'lZyb6kpfyLyRKG31'
COINBASE_SECRET = 'Nvn4oWqelwDdk46k4o6x96lUpmou5Tu6'
TELEGRAM_TOKEN = '5108384712:AAFwZz7hzeP1659GI1FddI84GFxbRAZkcvA'

coinbase_client = Client(COINBASE_KEY, COINBASE_SECRET)

def priceAlertLooperCallback(context):

    crypto = context.job.context[0]
    price = context.job.context[1]
    sign = context.job.context[2]
    chat_id = context.job.context[6]
    spot_price = coinbase_client.get_spot_price(currency_pair=crypto + '-USD')['amount']

    primerjalnik(sign, price, spot_price, crypto, context, chat_id)


def priceAlertCallback(context):
    crypto = context.job.context[0]
    sign = context.job.context[1]
    price = context.job.context[2]
    chat_id = context.job.context[3]
    spot_price = coinbase_client.get_spot_price(currency_pair=crypto + '-USD')['amount']

    primerjalnik(sign, price, spot_price, crypto, context, chat_id)


def primerjalnik(sign, price, spot_price, crypto, context, chat_id ):
    global send
    send = False

    if sign == '<':
        if float(price) >= float(spot_price):
            send = True
    else:
        if float(price) <= float(spot_price):
             send = True

    if send:
        response = f'👋 {crypto} has surpassed {price} and has just reached <b>{spot_price}$</b>!'
        context.bot.send_message(chat_id=chat_id, text=response)
        context.job.schedule_removal()