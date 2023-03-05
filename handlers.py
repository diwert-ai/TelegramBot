from utils import is_numeric, get_translated_text, setup_keyboard, gnews_keyboard

from db.userdata_db import UserDataDB
from engines.bullscows import BullsAndCowsEngine
from engines.google_ngrams import GoogleNgramsEngine
from engines.news_api import NewsAPIEngine
from engines.arxiv_api import ArxivEngine
from news_setup import NewsSetupConversation


class Handlers:
    def __init__(self):
        self.user_data_db = UserDataDB()
        self.news_engine = NewsAPIEngine()
        self.arxiv_engine = ArxivEngine()
        self.google_ngrams_engine = GoogleNgramsEngine()
        self.bulls_cows_engine = BullsAndCowsEngine()
        self.news_setup_conversation = NewsSetupConversation(self.user_data_db)

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

        context.user_data['news_setup'] = self.user_data_db.get_news_setup(chat.username)
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
            message = 'Enter topic: /news [topic]!'
            update.message.reply_text(message)

    def next_5_news(self, update, context):
        news_generator = self.news_engine.batch_generator
        print(f'news gen: {news_generator}')
        if news_generator:
            try:
                message = next(news_generator)
            except StopIteration as exc:
                print(f'StopIteration is appeared! {exc}')
                message = 'No more news! Batch pull is empty!'
        else:
            message = 'The news generator was not created!'

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
               'return to setup': self.return_setup}
        ops.get(text, self.just_translation)(update, context)
