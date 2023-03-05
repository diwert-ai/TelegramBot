from urllib import parse
from requests import get
from config import Config
from utils import get_translated_text


class NewsAPIEngine:
    def __init__(self):
        self.api_key = Config.news_api_key
        self.batch_generator = None

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

    def get_top5_news(self, topic, setup):
        print(setup)
        date_from, sort_by, lang = setup['date_from'], setup['sort_by'], setup['news_lang']
        topic_lang, headlines_lang = setup['topic_lang'], setup['headlines_lang']
        if topic_lang != lang:
            topic = get_translated_text(topic, destination=lang)
        data, message = self.run_query(topic, date_from=date_from, sort_by=sort_by, lang=lang), []
        status = data['status']
        total_results = data['totalResults']
        message.append(f'status: {status}\ntotal results: {total_results}')
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

    @staticmethod
    def batching(news_data, batch_size=5, headlines_lang='ru', lang='en'):
        total_results = news_data["totalResults"]
        articles = news_data['articles']
        start_line = f'status: {news_data["status"]}\ntotal results: {total_results}'
        print(start_line)
        if not total_results:
            while True:
                yield 'No news on this topic!'

        while True:
            for batch_start in range(0, total_results, batch_size):
                message = [start_line]
                for k, article in enumerate(articles[batch_start: batch_start + batch_size]):
                    title = article['title']
                    n = batch_start + k + 1
                    link, url = f"{article['source']['name']}: {title}", f"{article['url']}"
                    message.append(f'<a href="{url}">{n}. {link}</a>')
                    if headlines_lang != lang:
                        title = get_translated_text(title, destination=headlines_lang)
                    message.append(title)
                yield '\n'.join(message)

    def set_batch_generator(self, topic, setup):
        print(setup)
        date_from, sort_by, lang = setup['date_from'], setup['sort_by'], setup['news_lang']
        topic_lang, headlines_lang = setup['topic_lang'], setup['headlines_lang']
        if topic_lang != lang:
            topic = get_translated_text(topic, destination=lang)
        news_data = self.run_query(topic, date_from=date_from, sort_by=sort_by, lang=lang)
        self.batch_generator = self.batching(news_data, headlines_lang=headlines_lang, lang=lang)
