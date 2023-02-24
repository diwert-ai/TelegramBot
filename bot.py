import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import Config
from handlers import on_start_command, on_guess_command, on_text_message, on_ngram_command, on_decode_command


logging.basicConfig(filename='bot.log',
                    format='[%(asctime)s] [%(levelname)s] => %(message)s',
                    level=logging.INFO)


def main():
    bot = Updater(token=Config.telegram_bot_token)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', on_start_command))
    dp.add_handler(CommandHandler('g', on_guess_command))
    dp.add_handler(CommandHandler('ngram', on_ngram_command))
    dp.add_handler(CommandHandler('decode', on_decode_command))
    dp.add_handler(MessageHandler(Filters.text, on_text_message))

    logging.info('Bot is running...')
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
