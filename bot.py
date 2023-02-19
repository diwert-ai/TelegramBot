import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import Config
from handlers import on_start_command, on_guess_command, on_text_message


logging.basicConfig(filename='bot.log',
                    format='[%(asctime)s] [%(levelname)s] => %(message)s',
                    level=logging.INFO)


def main():
    bot = Updater(token=Config.token)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', on_start_command))
    dp.add_handler(CommandHandler('g', on_guess_command))
    dp.add_handler(MessageHandler(Filters.text, on_text_message))

    logging.info('Bot run')
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
