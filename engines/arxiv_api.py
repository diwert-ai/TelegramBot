import arxiv
from utils import get_translated_text


class ArxivEngine:
    def __init__(self):
        self.batch_generator = None
        self.search_results = None
        self.sort_by_map = {'relevance': arxiv.SortCriterion.Relevance,
                            'lastUpdatedDate': arxiv.SortCriterion.LastUpdatedDate,
                            'submittedDate': arxiv.SortCriterion.SubmittedDate}
        self.sort_order_map = {'descending': arxiv.SortOrder.Descending,
                               'ascending': arxiv.SortOrder.Ascending}

    @staticmethod
    def run_query(query, max_results, sort_by, sort_order):
        print(f'arxiv run query: {query} {max_results} {sort_by} {sort_order}')
        search = arxiv.Search(
            query='all:"'+query+'"',
            max_results=max_results,
            sort_by=sort_by,
            sort_order=sort_order
        )
        return search

    @staticmethod
    def get_arxiv_url(links):
        for url in links:
            if 'arxiv.org' in str(url):
                return url
        return links[0]

    def get_info(self, query):
        search = arxiv.Search(
            query='all:"'+query+'"',
            max_results=5,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        message = []
        for result in search.results():
            authors = ', '.join(map(lambda x: x.name, result.authors))
            link, url = f"{result.published} {authors}: {result.title}", f"{self.get_arxiv_url(result.links)}"
            message.append(f'<a href="{url}">{link}</a>')
            message.append(get_translated_text(result.title, destination='ru'))
            # message.append(get_translated_text(result.summary, destination='ru'))
            message.append('---------------------------')

        return '\n'.join(message) if message else 'no articles on this topic'

    def batching(self, batch_size=5, results_lang='ru', lang='en'):
        total_articles = len(list(self.search_results.results()))
        start_line = f'<b>total articles: {total_articles}</b>'
        print(start_line)
        if not total_articles:
            while True:
                yield 'No articles on this topic!'

        while True:
            articles = self.search_results.results()
            for batch_start in range(0, total_articles, batch_size):
                message = [start_line]
                for k in range(batch_size):
                    try:
                        article = next(articles)
                    except StopIteration:
                        break
                    title = article.title
                    authors = ', '.join(map(lambda x: x.name, article.authors))
                    link, url = f"{article.published} {authors}: {title}", f"{self.get_arxiv_url(article.links)}"
                    n = batch_start + k + 1
                    message.append(f'<a href="{url}">{n}. {link}</a>')
                    if results_lang != lang:
                        title = get_translated_text(title, destination=results_lang)
                    message.append(title)
                    message.append(f'<b>type /abs_{n} to get the article abstract</b>')
                    message.append('<b>---------------------------------------------------------------------</b>')
                yield '\n'.join(message)

    def set_batch_generator(self, topic, setup):
        print(setup)
        topic_lang, results_lang, lang = setup['topic_lang'], setup['results_lang'], 'en'
        max_results = setup['max_results']
        sort_by, sort_order = self.sort_by_map[setup['sort_by']], self.sort_order_map[setup['sort_order']]
        if topic_lang != lang:
            topic = get_translated_text(topic, destination=lang)
        self.search_results = self.run_query(topic, max_results, sort_by, sort_order)
        self.batch_generator = self.batching(results_lang=results_lang, lang=lang)
        return topic
