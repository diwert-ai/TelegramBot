import sqlite3

from config import Config


class NgramsDB:
    def __init__(self):
        self.ngrams_db_path = Config.ngrams_db_path

    def insert_ngrams(self, data):
        with sqlite3.connect(self.ngrams_db_path) as db:
            cursor = db.cursor()
            cursor.executemany('INSERT INTO ngrams(ngram, prob) VALUES(?, ?)', data)

    def select_ngrams(self, data):
        with sqlite3.connect(self.ngrams_db_path) as db:
            cursor = db.cursor()
            placeholders = '(' + ','.join('?' for _ in range(len(data))) + ')'
            query = 'SELECT ngram, prob FROM ngrams WHERE ngram IN ' + placeholders
            result = cursor.execute(query, data)

        return result.fetchall()
