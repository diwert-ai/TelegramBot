from random import choice
from string import digits
from requests import get, JSONDecodeError
from urllib import parse
from itertools import product
from datetime import datetime, timedelta
import sqlite3
import arxiv
from googletrans import Translator
from telegram import ReplyKeyboardMarkup

from config import Config


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


# https://www.geeksforgeeks.org/scrape-google-ngram-viewer-using-python/
def run_google_ngrams_query(query, start_year=2000, end_year=2019, corpus=26, smoothing=0):
    # converting a regular string to the standard URL format
    # eg: "geeks for,geeks" will convert to "geeks%20for%2Cgeeks"
    query = parse.quote(query)
    url = 'https://books.google.com/ngrams/json?content=' + query + \
          '&year_start=' + str(start_year) + '&year_end=' + \
          str(end_year) + '&corpus=' + str(corpus) + '&smoothing=' + \
          str(smoothing) + ''

    return get(url).json()


def db_insert_ngrams(data):
    with sqlite3.connect(Config.ngrams_db_path) as db:
        cursor = db.cursor()
        cursor.executemany('INSERT INTO ngrams(ngram, prob) VALUES(?, ?)', data)


def db_select_ngrams(data):
    with sqlite3.connect(Config.ngrams_db_path) as db:
        cursor = db.cursor()
        placeholders = '(' + ','.join('?' for _ in range(len(data))) + ')'
        query = 'SELECT ngram, prob FROM ngrams WHERE ngram IN ' + placeholders
        result = cursor.execute(query, data)

    return result.fetchall()


def db_register_user(user_data):
    with sqlite3.connect(Config.user_data_db_path) as db:
        cursor = db.cursor()
        query = 'SELECT id FROM users WHERE user_name = (?)'
        user_name = user_data['user_name']
        registered = cursor.execute(query, (user_name,)).fetchall()
        if not registered:
            first_name, last_name = user_data['first_name'], user_data['last_name']
            query = 'INSERT INTO users(user_name, first_name, last_name) VALUES(?, ?, ?)'
            cursor.execute(query, (user_name, first_name, last_name))

    return registered


def default_news_setup():
    return {'date_from': (datetime.today() - timedelta(days=20)).strftime('%Y-%m-%d'),
            'sort_by': 'relevancy',
            'topic_lang': 'en',
            'news_lang': 'en',
            'headlines_lang': 'ru'}


def db_update_news_setup(username, news_setup):
    """
    Updates table news_setup if record exists for user, else inserts user's
    news setup record in this table
    :param username: Telegram username
    :param news_setup: User's news setup dictionary
    :return: None
    """
    with sqlite3.connect(Config.user_data_db_path) as db:
        cursor = db.cursor()
        query = 'SELECT id FROM users WHERE user_name = (?)'
        result = cursor.execute(query, (username,)).fetchone()
        assert result, f'There is no record in table `users` for user {username}!'
        user_id = result[0]
        query = 'SELECT id FROM news_setup WHERE user_id = (?)'
        result = cursor.execute(query, (user_id,)).fetchone()
        if result:
            query = '''UPDATE news_setup 
                       SET date_from = (?),
                           sort_by = (?),
                           topic_lang = (?),
                           news_lang = (?),
                           headlines_lang = (?)
                       WHERE user_id = (?)'''
        else:
            query = '''INSERT INTO news_setup(date_from, sort_by, topic_lang, news_lang, headlines_lang, user_id)
                       VALUES(?, ?, ?, ?, ?, ?)'''

        cursor.execute(query, (news_setup['date_from'], news_setup['sort_by'], news_setup['topic_lang'],
                               news_setup['news_lang'], news_setup['headlines_lang'], user_id))


def db_get_news_setup(user_name):
    """
    Returns user's news setup dictionary from db if it exists,
    else returns default news setup.
    :param user_name: Username in telegram
    :return: User's news setup dictionary
    """
    news_setup = dict()
    with sqlite3.connect(Config.user_data_db_path) as db:
        cursor = db.cursor()
        query = '''SELECT date_from, sort_by, topic_lang, news_lang, headlines_lang
                   FROM news_setup ns
                   LEFT JOIN users u on u.id = ns.user_id
                   WHERE u.user_name = (?)'''
        result = cursor.execute(query, (user_name,)).fetchone()
        if result:
            news_setup = {'date_from': result[0],
                          'sort_by': result[1],
                          'topic_lang': result[2],
                          'news_lang': result[3],
                          'headlines_lang': result[4]}

    return news_setup if news_setup else default_news_setup()


# возвращает топ k=5 комбинаций букв (n-грамм) отсортированных по убыванию частоты
def top_k_ngrams(numeric_code, k=5):
    mapping = {'2': "abc", '3': "def", '4': "ghi", '5': "jkl", '6': "mno", '7': "pqrs", '8': "tuv", '9': "wxyz"}
    ngrams = list(map(''.join, product(*tuple(map(lambda x: mapping[x], numeric_code)))))
    print('Trying to get statistics from the database...', end=' ')
    ngrams_stat = db_select_ngrams(ngrams)
    if not ngrams_stat:
        print('data not found! :(')
        print('Trying to retrieve data from Google Ngram Viewer service...')
        ngrams_num, chunk_size = len(ngrams), 512
        print(f'ngrams total: {ngrams_num},  chunk size: {chunk_size}')
        for chunk_start in range(0, ngrams_num, chunk_size):
            print(f'Retrieving ngrams from {chunk_start} to {chunk_start + chunk_size}...')
            request = ','.join(ngrams[chunk_start:chunk_start + chunk_size])
            try:
                data = run_google_ngrams_query(request)
            except JSONDecodeError as error:
                print(f'JSONDecodeError is appeared! {error}')
                data = None
            for num, rec in enumerate(data, start=1):
                ngram, stat = rec['ngram'], rec['timeseries']
                freq = sum(stat) / len(stat) if stat else 0
                print(f'#{num} stats for "{rec["ngram"]}" is {freq}')
                ngrams_stat.append((ngram, freq))
        db_insert_ngrams(ngrams_stat)
    else:
        print('ok!')
    print(f'ngrams with stats total: {len(ngrams_stat)}, ngrams total: {len(ngrams)}')

    return sorted(ngrams_stat, key=lambda x: x[1], reverse=True)[:k]


def run_newsapi_query(query, date_from='2023-02-01', sort_by='relevancy', lang='en'):
    # converting a regular string to the standard URL format
    # eg: "geeks for,geeks" will convert to "geeks%20for%2Cgeeks"
    query = parse.quote(query)
    url = 'https://newsapi.org/v2/everything?q=' + query \
          + '&from=' + date_from \
          + '&sortBy=' + sort_by \
          + '&language=' + lang \
          + '&apiKey=' + Config.news_api_key

    print(url)

    return get(url).json()


def get_news(topic, setup):
    print(setup)
    date_from, sort_by, lang = setup['date_from'], setup['sort_by'], setup['news_lang']
    topic_lang, headlines_lang = setup['topic_lang'], setup['headlines_lang']
    if topic_lang != lang:
        topic = get_translated_text(topic, destination=lang)
    data, message = run_newsapi_query(topic, date_from=date_from, sort_by=sort_by, lang=lang), []
    articles = data['articles']
    for article in articles[:5]:
        title = article['title']
        link, url = f"{article['source']['name']}: {title}", f"{article['url']}"
        message.append(f'<a href="{url}">{link}</a>')
        if headlines_lang != lang:
            title = get_translated_text(title, destination=headlines_lang)
        message.append(title)
        # message.append('---------------------------')
    return '\n'.join(message) if message else 'no news on this topic'


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
    return Translator().translate(text, dest=destination).text
