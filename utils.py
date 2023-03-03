from string import digits
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
