from random import choice
from string import digits
from datetime import datetime, timedelta
import arxiv
import translators as ts
from telegram import ReplyKeyboardMarkup


def setup_keyboard():
    keys = [['news setup', 'arxiv setup']]
    return ReplyKeyboardMarkup(keys)


def is_numeric(string):
    for char in string:
        if char not in digits:
            return False
    return True


def get_bulls_cows_reply(user_string, magic_string):
    bulls, cows = sum([user_string[i] == magic_string[i] for i in range(4)]), 0
    for i, u_char in enumerate(user_string):
        if u_char in magic_string and magic_string[i] != user_string[i]:
            cows += 1

    return f'{bulls}B{cows}C'


def gen_magic_string():
    return ''.join([choice(digits) for _ in range(4)])


def default_news_setup():
    return {'date_from': (datetime.today() - timedelta(days=20)).strftime('%Y-%m-%d'),
            'sort_by': 'relevancy',
            'topic_lang': 'en',
            'news_lang': 'en',
            'headlines_lang': 'ru'}


def get_arxiv_info(query):
    search = arxiv.Search(
        query=query,
        max_results=3,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    message = []
    for result in search.results():
        authors = ', '.join(map(lambda x: x.name, result.authors))
        link, url = f"{result.published} {authors}: {result.title}", f"{result.links[0]}"
        message.append(f'<a href="{url}">{link}</a>')
        message.append(get_translated_text(result.title, destination='ru'))
        # message.append(get_translated_text(result.summary, destination='ru'))
        message.append('---------------------------')

    return '\n'.join(message) if message else 'no articles on this topic'


def get_translated_text(text, destination='en'):
    return ts.translate_text(query_text=text, to_language=destination, translator='google')
