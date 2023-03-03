from itertools import product
from urllib import parse
from requests import get, JSONDecodeError

from ngrams_db import NgramsDB


class GoogleNgramsEngine:
    def __init__(self):
        self.ngrams_db = NgramsDB()

    # https://www.geeksforgeeks.org/scrape-google-ngram-viewer-using-python/
    @staticmethod
    def run_query(query, start_year=2000, end_year=2019, corpus=26, smoothing=0):
        # converting a regular string to the standard URL format
        # eg: "geeks for,geeks" will convert to "geeks%20for%2Cgeeks"
        query = parse.quote(query)
        url = 'https://books.google.com/ngrams/json?content=' + query + \
              '&year_start=' + str(start_year) + '&year_end=' + \
              str(end_year) + '&corpus=' + str(corpus) + '&smoothing=' + \
              str(smoothing) + ''

        return get(url).json()

    def top_k_ngrams(self, numeric_code, k=5):
        mapping = {'2': "abc", '3': "def", '4': "ghi", '5': "jkl", '6': "mno", '7': "pqrs", '8': "tuv", '9': "wxyz"}
        ngrams = list(map(''.join, product(*tuple(map(lambda x: mapping[x], numeric_code)))))
        print('Trying to get statistics from the database...', end=' ')
        ngrams_stat = self.ngrams_db.select_ngrams(ngrams)
        if not ngrams_stat:
            print('data not found! :(')
            print('Trying to retrieve data from Google Ngram Viewer service...')
            ngrams_num, chunk_size = len(ngrams), 512
            print(f'ngrams total: {ngrams_num},  chunk size: {chunk_size}')
            for chunk_start in range(0, ngrams_num, chunk_size):
                print(f'Retrieving ngrams from {chunk_start} to {chunk_start + chunk_size}...')
                request = ','.join(ngrams[chunk_start:chunk_start + chunk_size])
                try:
                    data = self.run_query(request)
                except JSONDecodeError as error:
                    print(f'JSONDecodeError is appeared! {error}')
                    data = None
                for num, rec in enumerate(data, start=1):
                    ngram, stat = rec['ngram'], rec['timeseries']
                    freq = sum(stat) / len(stat) if stat else 0
                    print(f'#{num} stats for "{rec["ngram"]}" is {freq}')
                    ngrams_stat.append((ngram, freq))
            self.ngrams_db.insert_ngrams(ngrams_stat)
        else:
            print('ok!')
        print(f'ngrams with stats total: {len(ngrams_stat)}, ngrams total: {len(ngrams)}')

        return sorted(ngrams_stat, key=lambda x: x[1], reverse=True)[:k]
