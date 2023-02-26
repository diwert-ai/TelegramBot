import logging

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from config import Config

from handlers import (on_start_command, on_guess_command, on_echo_command,
                      on_ngram_command, on_decode_command, on_news_command,
                      on_arxiv_command, on_trans_command, do_translation)

from news_setup import (news_setup_start, news_setup_date_from,
                        news_setup_sort_up, news_setup_news_lang,
                        news_setup_topic_lang, news_setup_headlines_lang,
                        news_setup_fallback)

logging.basicConfig(filename='bot.log',
                    format='[%(asctime)s] [%(levelname)s] => %(message)s',
                    level=logging.INFO)


def main():
    bot = Updater(token=Config.telegram_bot_token)
    dp = bot.dispatcher
    news_setup = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(news setup)$'), news_setup_start)
        ],
        states={
            'date_from': [MessageHandler(Filters.regex(r'^([2][0][0-2]\d-[0-1]\d-[0-3]\d)$'),
                                         news_setup_date_from
                                         )
                          ],
            'sort_up': [MessageHandler(Filters.regex('^(relevancy|popularity|publishedAt)$'),
                                       news_setup_sort_up
                                       )
                        ],
            'news_lang': [MessageHandler(Filters.regex('^(ru|en|de|fr|it|es)$'),
                                         news_setup_news_lang
                                         )
                          ],
            'topic_lang': [MessageHandler(Filters.regex('^ru|en$'), news_setup_topic_lang)],
            'headlines_lang': [MessageHandler(Filters.regex('^ru|en$'), news_setup_headlines_lang)],

        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video
                           | Filters.document | Filters.audio | Filters.voice
                           | Filters.location, news_setup_fallback)
        ]
    )
    dp.add_handler(news_setup)
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
    main()
