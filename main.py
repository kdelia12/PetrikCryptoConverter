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
           "Example: bitcoin dollar 2.5 - \n" \
           "shows the price of 2.5 bitcoins in US dollars.\n" \
           "Use /help for other options."
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "/help - shows this message.\n" \
           "/curr - gives a list of supported currencies.\n" \
           "<cur1> <cur2> <quantity> - shows the price\n" \
           "of <quantity> units of <cur1> in <cur2>.\n" \
           "Example: bitcoin dollar 2.5 - shows the price\n" \
           "of 2.5 bitcoin in US dollars\n"
    bot.reply_to(message, text)

@bot.message_handler(commands=['curr'])
def list_of(message: telebot.types.Message):
    text = 'Available currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
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
            total_base_formatted = format(total_base, ".5f").rstrip("0")
        else: total_base_formatted = str(total_base)

        # If the formatted value ends in a decimal point, remove it to

    text = f'Price {amount} {base.upper()} in {quote.upper()} = {total_base_formatted}'
    bot.send_message(message.chat.id, text)

bot.polling()


#def main():
#    test()

#if __name__ == '__main__':
#    main()

# End of file
