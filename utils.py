from string import digits
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


def get_translated_text(text, destination='en'):
    return ts.translate_text(query_text=text, to_language=destination, translator='google')
