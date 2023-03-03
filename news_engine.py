from urllib import parse
from requests import get
from config import Config
from utils import get_translated_text


class NewsAPIEngine:
    def __init__(self):
        self.api_key = Config.news_api_key

    def run_query(self, query, date_from='2023-02-01', sort_by='relevancy', lang='en'):
        # converting a regular string to the standard URL format
        # eg: "geeks for,geeks" will convert to "geeks%20for%2Cgeeks"
        query = parse.quote(query)
        url = 'https://newsapi.org/v2/everything?q=' + query \
              + '&from=' + date_from \
              + '&sortBy=' + sort_by \
              + '&language=' + lang \
              + '&apiKey=' + self.api_key

        print(url)

        return get(url).json()

    def get_news(self, topic, setup):
        print(setup)
        date_from, sort_by, lang = setup['date_from'], setup['sort_by'], setup['news_lang']
        topic_lang, headlines_lang = setup['topic_lang'], setup['headlines_lang']
        if topic_lang != lang:
            topic = get_translated_text(topic, destination=lang)
        data, message = self.run_query(topic, date_from=date_from, sort_by=sort_by, lang=lang), []
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