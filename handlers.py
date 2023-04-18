from utils import is_numeric, get_translated_text, setup_keyboard, gnews_keyboard, garxiv_keyboard

from db.userdata_db import UserDataDB
from engines.bullscows import BullsAndCowsEngine
from engines.google_ngrams import GoogleNgramsEngine
from engines.news_api import NewsAPIEngine
from engines.arxiv_api import ArxivEngine
from news_setup import NewsSetupConversation
from arxiv_setup import ArxivSetupConversation


class Handlers:
    def __init__(self):
        self.user_data_db = UserDataDB()
        self.news_engine = NewsAPIEngine()
        self.arxiv_engine = ArxivEngine()
        self.google_ngrams_engine = GoogleNgramsEngine()
        self.bulls_cows_engine = BullsAndCowsEngine()
        self.news_setup_conversation = NewsSetupConversation(self.user_data_db)
        self.arxiv_setup_conversation = ArxivSetupConversation(self.user_data_db)

    @staticmethod
    def help(update, context):
        print('Help event message received!')
        print(f'update: {update}')
        message = """
This bot supports the following commands:
0. 'help' - show this message!
1. 'start' - more info here: /start_info 
2. 'g' or 'guess' - more info here: /guess_info
3. 'ngram' - more info here: /ngram_info
4. 'decode' - more info here: /decode_info 
5. 'news' - more info here: /news_info
6. 'gnews' - more info here: /gnews_info
7. 'arxiv' - more info here: /arxiv_info
8. 'garxiv' - more info here: /garxiv_info
9. 'trans' - more info here: /trans_info
10. 'echo' - more info here: /echo_info

The bot returns an echo in English to any normal text message :)
"""

        update.message.reply_text(message, reply_markup=setup_keyboard())

    @staticmethod
    def info(update, context):
        info_msgs = {'/start_info': """
`/start` - The bot responds with a greeting, using the username. It finds out if the user has been there before and 
if not, it registers this user in the sqlite database. A menu appears with two buttons:
`news setup` and `arxiv setup`. The first launches the conversation to create user parameters for requests 
to https://newsapi.org (used in the `/news` and `/gnews` commands). The second launches the conversation to create user 
parameters for requests to https://arxiv.org (used in the `/arxiv` and `/garxiv` commands). User parameters are stored
in `context.user_data` and stored in the sqlite database.
""",

                     '/guess_info': """
`/g [4-digits string - user's guess]` or `/guess [4-digits string - user's guess]` - Bot plays a game of bulls and cows.
The bot guesses a four-digit number and returns the number of bulls and cows according to the user's guess in the format 
nBmC, where n is the number of bulls and m is the number of cows.
""",
                     '/ngram_info': """
`/ngram [n-gram]` - Bot returns n-gram statistics requested from Google Ngram Viewer service.
""",
                     '/decode_info': """
`/decode [numeric code]` - The bot returns the most likely decoding of the number string.
Each digit is recoded according to the rules of the keypad of a pushbutton phone. The probability is determined by
the n-gram statistics obtained from the Google Ngram Viewer service. The n-gram stats are saved in a sqlite database,
which allows you to take the stats from the database instead of making the same queries to the Google Ngram Viewer.
""",
                     '/news_info': """
`/news [topic]` - The bot returns the top 5 news items with a given topic, using the service https://newsapi.org
with the parameters that have been configured in `news setup` conversation
""",
                     '/gnews_info': """
`/gnews [topic]` - The bot does the same thing as the `/news` command, but a menu appears with the commands
`next 5 news` (gives the next 5 news from the general pool that the https://newsapi.org service has returned) and
`return setup` (returns the `news setup` and `arxiv setup` menu buttons - see step 1). Showing news on the button
`next 5 news` is looped to an endless loop, ie, after the last news from the pool will be shown, the show will again
start with the first news.
""",
                     '/arxiv_info': """
`/arxiv [topic]` - The bot returns the last 5 articles with the given topic, published on https://arxiv.org
""",
                     '/garxiv_info': """
`/garxiv [topic]` - The bot does the same thing as the `/arxiv` command, but a menu appears with the commands
`next 5 articles` (gives the next 5 articles from the general pool that the https://arxiv.org service has returned) and
`return setup` (returns the `news setup` and `arxiv setup` menu buttons - see step 1). Showing articles on the button
`next 5 articles` is looped to an endless loop, ie, after the last article from the pool will be shown, the show will 
again start with the first article.
""",
                     '/trans_info': """
`/trans [phrase]` - The bot returns the translation of the phrase from Russian to English                     
""",
                     '/echo_info': """
`/echo [text]` - The bot just reply with an echo text
"""}
        update.message.reply_text(info_msgs.get(update.message.text, 'info is coming!'), reply_markup=setup_keyboard())

    def start(self, update, context):
        print('Start event message received!')
        print(f'update: {update}')
        chat = update.message.chat
        user_data = {'user_name': chat.username,
                     'first_name': chat.first_name,
                     'last_name': chat.last_name}
        db_user_status = self.user_data_db.register_user(user_data)
        print(f'register status: {db_user_status}')
        if db_user_status:
            message = f'Long time no see! Hi, {chat.username}! 🤝'
        else:
            message = f'Sounds like this is your first time here! 🙂 Welcome, {chat.username}! 😉'

        message += "\nInformation on the bot's commands is here: /help"

        context.user_data['news_setup'] = self.user_data_db.get_news_setup(chat.username)
        context.user_data['arxiv_setup'] = self.user_data_db.get_arxiv_setup(chat.username)
        update.message.reply_text(message, reply_markup=setup_keyboard())

    def guess(self, update, context):
        print('Guess event message received!')
        print(f'update: {update}')
        print(f'context.user_data: {context.user_data}')
        if 'magic' not in context.user_data:
            context.user_data['magic'] = self.bulls_cows_engine.new_guess()
        magic_string = context.user_data['magic']
        print(f'magic number: {magic_string}')
        args = context.args
        print(f'context.args: {args}')
        if args and len(args[0]) == 4 and is_numeric(args[0]):
            user_string = args[0]
            print(f'user_string: {user_string}, magic_string: {magic_string}')
            bulls_cows_reply = self.bulls_cows_engine.get_bulls_and_cows(user_string, magic_string)
            message = f'{bulls_cows_reply}'
            if bulls_cows_reply[0] == '4':
                del context.user_data['magic']
                message += ' Guessed right! 👍'

        else:
            message = 'Enter string of 4 digits!'
        update.message.reply_text(message)

    def ngram(self, update, context):
        print('Ngram event message received!')
        args = context.args
        print(f'args: {args}')
        if args:
            user_string = args[0]
            print(f'user_string: {user_string}')
            stat = self.google_ngrams_engine.run_query(user_string)
        else:
            stat = None

        update.message.reply_text(f'{stat}')

    def decode(self, update, context):
        print('Decode event message received!')
        args = context.args
        print(f'args: {args}')
        if args and is_numeric(user_string := args[0]) and ('0' not in user_string) and ('1' not in user_string):
            print(f'user_string: {user_string}')
            message = ', '.join(ngram[0] for ngram in self.google_ngrams_engine.top_k_ngrams(user_string))
        else:
            message = 'Code must be numeric without `0` and `1` characters!'

        update.message.reply_text(message)

    def news(self, update, context):
        print('News event message received!')
        args = context.args
        print(f'args: {args}')
        if args:
            user_string = ' '.join(args)
            username = update.message.chat.username
            print(f'username: {username}, user_string: {user_string}')
            if 'news_setup' in context.user_data:
                news_setup = context.user_data['news_setup']
            else:
                news_setup = self.user_data_db.get_news_setup(username)
            message = self.news_engine.get_top5_news(user_string, news_setup)
        else:
            message = 'Enter topic: /news [topic]!'

        update.message.reply_text(message, parse_mode='html')

    def gnews(self, update, context):
        print('News event message received!')
        args = context.args
        print(f'args: {args}')
        if args:
            user_string = ' '.join(args)
            username = update.message.chat.username
            print(f'username: {username}, user_string: {user_string}')
            if 'news_setup' in context.user_data:
                news_setup = context.user_data['news_setup']
            else:
                news_setup = self.user_data_db.get_news_setup(username)
            self.news_engine.set_batch_generator(user_string, news_setup)
            self.next_5_news(update, context)
        else:
            message = 'Enter topic: /gnews [topic]!'
            update.message.reply_text(message)

    def next_5_news(self, update, context):
        news_generator = self.news_engine.batch_generator
        print(f'news gen: {news_generator}')
        if news_generator:
            message = next(news_generator)
        else:
            message = 'The news generator was not created! Try first `/gnews [topic]` command!'

        update.message.reply_text(message, parse_mode='html', reply_markup=gnews_keyboard())

    @staticmethod
    def return_setup(update, context):
        update.message.reply_text('ok', reply_markup=setup_keyboard())

    def arxiv(self, update, context):
        print('Arxiv event message received!')
        args = context.args
        print(f'args: {args}')
        if args:
            user_string = ' '.join(args)
            print(f'user_string: {user_string}')
            message = self.arxiv_engine.get_info(user_string)
        else:
            message = 'Enter topic: /arxiv [topic]!'

        '''msgs = [message[i:i + 4096] for i in range(0, len(message), 4096)]
        for text in msgs:
            update.message.reply_text(text, parse_mode='html')'''

        update.message.reply_text(message, parse_mode='html')

    def garxiv(self, update, context):
        print('Garxiv event message received!')
        args = context.args
        print(f'args: {args}')
        if args:
            user_string = ' '.join(args)
            username = update.message.chat.username
            print(f'username: {username}, user_string: {user_string}')
            if 'arxiv_setup' in context.user_data:
                arxiv_setup = context.user_data['arxiv_setup']
            else:
                arxiv_setup = self.user_data_db.get_arxiv_setup(username)
            self.arxiv_engine.set_batch_generator(user_string, arxiv_setup)
            self.next_5_articles(update, context)
        else:
            message = 'Enter topic: /garxiv [topic]!'
            update.message.reply_text(message)

    def next_5_articles(self, update, context):
        articles_generator = self.arxiv_engine.batch_generator
        print(f'arxiv gen: {articles_generator}')
        if articles_generator:
            message = next(articles_generator)
        else:
            message = 'The arxiv articles generator was not created! Try first `/garxiv [topic]` command!'

        update.message.reply_text(message, parse_mode='html', reply_markup=garxiv_keyboard())

    @staticmethod
    def echo(update, context):
        print('Echo event message received!')
        args = context.args
        print(f'args: {args}')
        if args:
            user_string = ' '.join(args)
            print(f'user_string: {user_string}')
            message = user_string
        else:
            message = 'Enter text please!'
        update.message.reply_text(message)

    @staticmethod
    def trans(update, context):
        print('Trans event message received!')
        args = context.args
        print(f'args: {args}')
        if args:
            user_string = ' '.join(args)
            print(f'user_string: {user_string}')
            message = get_translated_text(user_string)
        else:
            message = 'Enter text to translate!'

        update.message.reply_text(message)

    @staticmethod
    def just_translation(update, context):
        update.message.reply_text(get_translated_text(update.message.text))

    def text_message_wrapper(self, update, context):
        text = update.message.text
        print(f'Text message received! Text: {text}')
        ops = {'next 5 news': self.next_5_news,
               'next 5 articles': self.next_5_articles,
               'return to setup': self.return_setup}
        ops.get(text, self.just_translation)(update, context)
