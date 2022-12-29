'''
A Telegram bot that convert a currency into another.
Example:
In Telegram: bitcoin dollar 2
- shows the price of 2 bitcoins in US dollars.
Also options are available in the bot.
Use /help for the full list of options.
'''

import telebot

from config import keys, TOKEN
from utils import CryptoConverter, CryptoConvertBotException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Convert a currency into another.\n" \
           "Example: /convert 1 btc idr - \n" \
           "shows the price of 1 bitcoins in US dollars.\n" \
           "Use /help for other options."
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "/help - shows this message.\n" \
           "Example: /convert 1 btc idr - shows the price\n" \
           "of 1 bitcoin in US dollars\n"
    bot.reply_to(message, text)


@bot.message_handler(commands=['convert'])
def convert(message: telebot.types.Message):
    if '/convert' not in message.text:
        # The command is not present in the message, so do not try to process it
        return

    try:
        values = message.text.split()

        if len(values) != 4:
            raise CryptoConvertBotException('Not three parameters')

        amount, base, quote,  = values[1:]  # Skip the first element, which is the command
        total_base = CryptoConverter.convert(base.upper(), quote.upper(),amount.upper()) 
    except CryptoConvertBotException as e:
        bot.reply_to(message, f'User error.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Could not process command\n{e}')

    else:
        if total_base  < 1:  # Check if total_base has a decimal part
            total_base = format(total_base, ".5f").rstrip("0")
        else: total_base

        # If the formatted value ends in a decimal point, remove it to

    text = f'Price {amount} {base.upper()} in {quote.upper()} = {total_base}'
    bot.reply_to(message, text)
    #add log
    print(message.from_user.username, message.text, total_base)

bot.polling()


#def main():
#    test()

#if __name__ == '__main__':
#    main()

# End of file
