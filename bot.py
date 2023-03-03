import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import Config

from handlers import (on_start_command, on_guess_command, on_echo_command,
                      on_ngram_command, on_decode_command, on_news_command,
                      on_arxiv_command, on_trans_command, do_translation)

from news_setup import NewsSetupConversation


def main():
    bot = Updater(token=Config.telegram_bot_token)
    dp = bot.dispatcher
    news_setup_handler = NewsSetupConversation().handler()
    dp.add_handler(news_setup_handler)
    dp.add_handler(CommandHandler('start', on_start_command))
    dp.add_handler(CommandHandler('g', on_guess_command))
    dp.add_handler(CommandHandler('guess', on_guess_command))
    dp.add_handler(CommandHandler('ngram', on_ngram_command))
    dp.add_handler(CommandHandler('decode', on_decode_command))
    dp.add_handler(CommandHandler('news', on_news_command))
    dp.add_handler(CommandHandler('arxiv', on_arxiv_command))
    dp.add_handler(CommandHandler('trans', on_trans_command))
    dp.add_handler(CommandHandler('echo', on_echo_command))
    dp.add_handler(MessageHandler(Filters.text, do_translation))

    logging.info('Bot is running...')
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    logging.basicConfig(filename='bot.log',
                        format='[%(asctime)s] [%(levelname)s] => %(message)s',
                        level=logging.INFO)
    main()
