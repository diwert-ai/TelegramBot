from string import digits
import translators as ts
from telegram import ReplyKeyboardMarkup
import pandas as pd
import matplotlib


def setup_keyboard():
    keys = [['news setup', 'arxiv setup']]
    return ReplyKeyboardMarkup(keys)


def gnews_keyboard():
    keys = [['next 5 news', 'return to setup']]
    return ReplyKeyboardMarkup(keys)


def garxiv_keyboard():
    keys = [['next 5 articles', 'diagram stat', 'return to setup']]
    return ReplyKeyboardMarkup(keys)


def is_numeric(string):
    for char in string:
        if char not in digits:
            return False
    return True


def get_translated_text(text, destination='en'):
    try:
        translated_text = ts.translate_text(query_text=text, to_language=destination, translator='google')
    except Exception as e:
        print(e)
        translated_text = f'<b>[Error occurred while translating 😞]</b>'

    return translated_text


def store_diagram(articles):
    matplotlib.use('agg')
    df = pd.DataFrame([vars(article) for article in articles])
    df = df[['title', 'published']]
    df_count = df['published'].groupby(df['published'].dt.year).count()
    print(df_count)
    fig = df_count.plot(kind='bar').get_figure()
    fig.savefig('diag.png')
