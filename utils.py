from random import choice
from string import digits
from requests import get, JSONDecodeError
from urllib import parse
from itertools import product
from datetime import datetime, timedelta
import arxiv
import translators as ts
from telegram import ReplyKeyboardMarkup

from ngrams_db import NgramsDB


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


def default_news_setup():
    return {'date_from': (datetime.today() - timedelta(days=20)).strftime('%Y-%m-%d'),
            'sort_by': 'relevancy',
            'topic_lang': 'en',
            'news_lang': 'en',
            'headlines_lang': 'ru'}


# возвращает топ k=5 комбинаций букв (n-грамм) отсортированных по убыванию частоты
def top_k_ngrams(numeric_code, k=5):
    ngrams_db = NgramsDB()
    mapping = {'2': "abc", '3': "def", '4': "ghi", '5': "jkl", '6': "mno", '7': "pqrs", '8': "tuv", '9': "wxyz"}
    ngrams = list(map(''.join, product(*tuple(map(lambda x: mapping[x], numeric_code)))))
    print('Trying to get statistics from the database...', end=' ')
    ngrams_stat = ngrams_db.select_ngrams(ngrams)
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
        ngrams_db.insert_ngrams(ngrams_stat)
    else:
        print('ok!')
    print(f'ngrams with stats total: {len(ngrams_stat)}, ngrams total: {len(ngrams)}')

    return sorted(ngrams_stat, key=lambda x: x[1], reverse=True)[:k]


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
