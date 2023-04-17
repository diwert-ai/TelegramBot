from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import MessageHandler, Filters, ConversationHandler
from utils import setup_keyboard


class ArxivSetupConversation:
    def __init__(self, userdata_db):
        self.userdata_db = userdata_db
        self.key = 'arxiv_setup'

    @staticmethod
    def sort_by_keyboard():
        return ReplyKeyboardMarkup([['relevance', 'lastUpdatedDate', 'submittedDate']], one_time_keyboard=True)

    @staticmethod
    def sort_order_keyboard():
        return ReplyKeyboardMarkup([['descending', 'ascending']], one_time_keyboard=True)

    @staticmethod
    def topic_lang_keyboard():
        return ReplyKeyboardMarkup([['ru', 'en']], one_time_keyboard=True)

    @staticmethod
    def results_lang_keyboard():
        return ReplyKeyboardMarkup([['ru', 'en']], one_time_keyboard=True)

    def start(self, update, context):
        update.message.reply_text('Welcome to arXiv service settings!\n' +
                                  "I'm going to ask you a few questions. - Pay attention!\n" +
                                  "Let's go!")
        update.message.reply_text('1. Select the sort criterion for results',
                                  reply_markup=self.sort_by_keyboard())
        return 'sort_by'

    def sort_by(self, update, context):
        context.user_data[self.key] = {'sort_by': update.message.text}
        update.message.reply_text('2. Select the sort order for results',
                                  reply_markup=self.sort_order_keyboard())
        return 'sort_order'

    def sort_order(self, update, context):
        context.user_data[self.key]['sort_order'] = update.message.text
        update.message.reply_text('3. Specify the maximum number of results to be returned in an execution of search',
                                  reply_markup=ReplyKeyboardRemove())
        return 'max_results'

    def max_results(self, update, context):
        context.user_data[self.key]['max_results'] = update.message.text
        update.message.reply_text('4. Select the language in which you will formulate the topic of the articles',
                                  reply_markup=self.topic_lang_keyboard())
        return 'topic_lang'

    def topic_lang(self, update, context):
        context.user_data[self.key]['topic_lang'] = update.message.text
        update.message.reply_text('5. Select the language in which you want to translate the results',
                                  reply_markup=self.results_lang_keyboard())
        return 'results_lang'

    def results_lang(self, update, context):
        context.user_data[self.key]['results_lang'] = update.message.text
        username = update.message.chat.username
        user_arxiv_setup = context.user_data[self.key]
        message = f'''Thanks! Your arxiv setup:
<b>Sort by</b>: {user_arxiv_setup['sort_by']}
<b>Sort order</b>: {user_arxiv_setup['sort_order']}
<b>Maximum results</b>: {user_arxiv_setup['max_results']}
<b>Topic language</b>: {user_arxiv_setup['topic_lang']}
<b>Results language</b>: {user_arxiv_setup['results_lang']}'''
        self.userdata_db.update_arxiv_setup(username, user_arxiv_setup)
        update.message.reply_text(message, parse_mode='html', reply_markup=setup_keyboard())
        update.message.reply_text('Arxiv setup have stored to db!')
        return ConversationHandler.END

    @staticmethod
    def fallback(update, context):
        update.message.reply_text('Wrong input! Please do it again!')

    def handler(self):
        return ConversationHandler(
            entry_points=[
                MessageHandler(Filters.regex('^(arxiv setup)$'), self.start)
            ],
            states={
                'sort_by': [MessageHandler(Filters.regex('^(relevance|lastUpdatedDate|submittedDate)$'),
                                           self.sort_by
                                           )
                            ],
                'sort_order': [MessageHandler(Filters.regex('^(descending|ascending)$'),
                                              self.sort_order
                                              )
                               ],
                'max_results': [MessageHandler(Filters.regex(r'^(\d+)$'),
                                               self.max_results
                                               )
                                ],
                'topic_lang': [MessageHandler(Filters.regex('^ru|en$'), self.topic_lang)],
                'results_lang': [MessageHandler(Filters.regex('^ru|en$'), self.results_lang)],

            },
            fallbacks=[
                MessageHandler(Filters.text | Filters.photo | Filters.video
                               | Filters.document | Filters.audio | Filters.voice
                               | Filters.location, self.fallback)
            ]
        )
