import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import Config
from handlers import Handlers


def main():
    bot = Updater(token=Config.telegram_bot_token)
    dp = bot.dispatcher
    handlers = Handlers()
    dp.add_handler(handlers.news_setup_conversation.handler())
    dp.add_handler(CommandHandler('help', handlers.help))
    dp.add_handler(CommandHandler('start_info', handlers.info))
    dp.add_handler(CommandHandler('guess_info', handlers.info))
    dp.add_handler(CommandHandler('ngram_info', handlers.info))
    dp.add_handler(CommandHandler('decode_info', handlers.info))
    dp.add_handler(CommandHandler('news_info', handlers.info))
    dp.add_handler(CommandHandler('gnews_info', handlers.info))
    dp.add_handler(CommandHandler('arxiv_info', handlers.info))
    dp.add_handler(CommandHandler('trans_info', handlers.info))
    dp.add_handler(CommandHandler('echo_info', handlers.info))
    dp.add_handler(CommandHandler('start', handlers.start))
    dp.add_handler(CommandHandler('g', handlers.guess))
    dp.add_handler(CommandHandler('guess', handlers.guess))
    dp.add_handler(CommandHandler('ngram', handlers.ngram))
    dp.add_handler(CommandHandler('decode', handlers.decode))
    dp.add_handler(CommandHandler('news', handlers.news))
    dp.add_handler(CommandHandler('gnews', handlers.gnews))
    dp.add_handler(CommandHandler('arxiv', handlers.arxiv))
    dp.add_handler(CommandHandler('trans', handlers.trans))
    dp.add_handler(CommandHandler('echo', handlers.echo))
    dp.add_handler(MessageHandler(Filters.text, handlers.text_message_wrapper))
    logging.info('Bot is running...')
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    logging.basicConfig(filename='bot.log',
                        format='[%(asctime)s] [%(levelname)s] => %(message)s',
                        level=logging.INFO)
    main()
