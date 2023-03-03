import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import Config
from handlers import Handlers
from news_setup import NewsSetupConversation


def main():
    bot = Updater(token=Config.telegram_bot_token)
    dp = bot.dispatcher
    handlers = Handlers()
    news_setup_handler = NewsSetupConversation().handler()
    dp.add_handler(news_setup_handler)
    dp.add_handler(CommandHandler('start', handlers.start))
    dp.add_handler(CommandHandler('g', handlers.guess))
    dp.add_handler(CommandHandler('guess', handlers.guess))
    dp.add_handler(CommandHandler('ngram', handlers.ngram))
    dp.add_handler(CommandHandler('decode', handlers.decode))
    dp.add_handler(CommandHandler('news', handlers.news))
    dp.add_handler(CommandHandler('arxiv', handlers.arxiv))
    dp.add_handler(CommandHandler('trans', handlers.trans))
    dp.add_handler(CommandHandler('echo', handlers.echo))
    dp.add_handler(MessageHandler(Filters.text, handlers.translation))
    logging.info('Bot is running...')
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    logging.basicConfig(filename='bot.log',
                        format='[%(asctime)s] [%(levelname)s] => %(message)s',
                        level=logging.INFO)
    main()
