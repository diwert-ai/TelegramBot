import arxiv
from utils import get_translated_text


class ArxivEngine:
    @staticmethod
    def get_info(query):
        search = arxiv.Search(
            query=query,
            max_results=5,
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
