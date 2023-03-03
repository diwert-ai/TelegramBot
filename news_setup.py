from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import MessageHandler, Filters, ConversationHandler
from utils import setup_keyboard


class NewsSetupConversation:
    def __init__(self, userdata_db):
        self.userdata_db = userdata_db

    @staticmethod
    def sort_up_keyboard():
        return ReplyKeyboardMarkup([['relevancy', 'popularity', 'publishedAt']], one_time_keyboard=True)

    @staticmethod
    def news_lang_keyboard():
        return ReplyKeyboardMarkup([['ru', 'en', 'de', 'fr', 'it', 'es']], one_time_keyboard=True)

    @staticmethod
    def topic_lang_keyboard():
        return ReplyKeyboardMarkup([['ru', 'en']], one_time_keyboard=True)

    @staticmethod
    def headlines_lang_keyboard():
        return ReplyKeyboardMarkup([['ru', 'en']], one_time_keyboard=True)

    @staticmethod
    def start(update, context):
        update.message.reply_text("Welcome to news service settings!\n" +
                                  "I'm going to ask you a few questions. - Pay attention!\n" +
                                  "Let's go!")
        update.message.reply_text("1. Specify the date from which the news was published (format: yyyy-mm-dd)",
                                  reply_markup=ReplyKeyboardRemove())
        return 'date_from'

    def date_from(self, update, context):
        context.user_data['news_setup'] = {'date_from': update.message.text}
        update.message.reply_text('2. Select the order in which the news is sorted',
                                  reply_markup=self.sort_up_keyboard())
        return 'sort_by'

    def sort_by(self, update, context):
        context.user_data['news_setup']['sort_by'] = update.message.text
        update.message.reply_text('3. Select a news language',
                                  reply_markup=self.news_lang_keyboard())
        return 'news_lang'

    def news_lang(self, update, context):
        context.user_data['news_setup']['news_lang'] = update.message.text
        update.message.reply_text('4. Select the language in which you will formulate the topic of the news',
                                  reply_markup=self.topic_lang_keyboard())
        return 'topic_lang'

    def topic_lang(self, update, context):
        context.user_data['news_setup']['topic_lang'] = update.message.text
        update.message.reply_text('5. Select the language in which you want to translate the headlines',
                                  reply_markup=self.headlines_lang_keyboard())
        return 'headlines_lang'

    def headlines_lang(self, update, context):
        context.user_data['news_setup']['headlines_lang'] = update.message.text
        username = update.message.chat.username
        user_news_setup = context.user_data['news_setup']
        message = f'''Thanks! Your news setup:
<b>Date from</b>: {user_news_setup['date_from']}
<b>Sort by</b>: {user_news_setup['sort_by']}
<b>News language</b>: {user_news_setup['news_lang']}
<b>Topic language</b>: {user_news_setup['topic_lang']}
<b>Headlines language</b>: {user_news_setup['headlines_lang']}'''
        self.userdata_db.update_news_setup(username, user_news_setup)
        update.message.reply_text(message, parse_mode='html', reply_markup=setup_keyboard())
        update.message.reply_text('News setup have stored to db!')
        return ConversationHandler.END

    @staticmethod
    def fallback(update, context):
        update.message.reply_text('Wrong input! Please do it again!')

    def handler(self):
        return ConversationHandler(
            entry_points=[
                MessageHandler(Filters.regex('^(news setup)$'), self.start)
            ],
            states={
                'date_from': [MessageHandler(Filters.regex(r'^([2][0][0-2]\d-[0-1]\d-[0-3]\d)$'),
                                             self.date_from
                                             )
                              ],
                'sort_by': [MessageHandler(Filters.regex('^(relevancy|popularity|publishedAt)$'),
                                           self.sort_by
                                           )
                            ],
                'news_lang': [MessageHandler(Filters.regex('^(ru|en|de|fr|it|es)$'),
                                             self.news_lang
                                             )
                              ],
                'topic_lang': [MessageHandler(Filters.regex('^ru|en$'), self.topic_lang)],
                'headlines_lang': [MessageHandler(Filters.regex('^ru|en$'), self.headlines_lang)],

            },
            fallbacks=[
                MessageHandler(Filters.text | Filters.photo | Filters.video
                               | Filters.document | Filters.audio | Filters.voice
                               | Filters.location, self.fallback)
            ]
        )
