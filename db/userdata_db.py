import sqlite3
from datetime import datetime, timedelta

from config import Config


class UserDataDB:
    def __init__(self):
        self.user_data_db_path = Config.user_data_db_path

    @staticmethod
    def default_news_setup():
        return {'date_from': (datetime.today() - timedelta(days=20)).strftime('%Y-%m-%d'),
                'sort_by': 'relevancy',
                'topic_lang': 'en',
                'news_lang': 'en',
                'headlines_lang': 'ru'}

    @staticmethod
    def default_arxiv_setup():
        return {'sort_by': 'relevance',
                'sort_order': 'descending',
                'max_results': 10,
                'topic_lang': 'en',
                'results_lang': 'ru'}

    def register_user(self, user_data):
        with sqlite3.connect(self.user_data_db_path) as db:
            cursor = db.cursor()
            query = 'SELECT id FROM users WHERE user_name = (?)'
            user_name = user_data['user_name']
            registered = cursor.execute(query, (user_name,)).fetchall()
            if not registered:
                first_name, last_name = user_data['first_name'], user_data['last_name']
                query = 'INSERT INTO users(user_name, first_name, last_name) VALUES(?, ?, ?)'
                cursor.execute(query, (user_name, first_name, last_name))

        return registered

    def update_news_setup(self, username, news_setup):
        """
        Updates table news_setup if record exists for user, else inserts user's
        news setup record in this table
        :param username: Telegram username
        :param news_setup: User's news setup dictionary
        :return: None
        """
        with sqlite3.connect(self.user_data_db_path) as db:
            cursor = db.cursor()
            query = 'SELECT id FROM users WHERE user_name = (?)'
            result = cursor.execute(query, (username,)).fetchone()
            assert result, f'There is no record in table `users` for user {username}!'
            user_id = result[0]
            query = 'SELECT id FROM news_setup WHERE user_id = (?)'
            result = cursor.execute(query, (user_id,)).fetchone()
            if result:
                query = '''UPDATE news_setup 
                           SET date_from = (?),
                               sort_by = (?),
                               topic_lang = (?),
                               news_lang = (?),
                               headlines_lang = (?)
                           WHERE user_id = (?)'''
            else:
                query = '''INSERT INTO news_setup(date_from, sort_by, topic_lang, news_lang, headlines_lang, user_id)
                           VALUES(?, ?, ?, ?, ?, ?)'''

            cursor.execute(query, (news_setup['date_from'], news_setup['sort_by'], news_setup['topic_lang'],
                                   news_setup['news_lang'], news_setup['headlines_lang'], user_id))

    def get_news_setup(self, user_name):
        """
        Returns user's news setup dictionary from db if it exists,
        else returns default news setup.
        :param user_name: Username in telegram
        :return: User's news setup dictionary
        """
        news_setup = dict()
        with sqlite3.connect(self.user_data_db_path) as db:
            cursor = db.cursor()
            query = '''SELECT date_from, sort_by, topic_lang, news_lang, headlines_lang
                       FROM news_setup ns
                       LEFT JOIN users u on u.id = ns.user_id
                       WHERE u.user_name = (?)'''
            result = cursor.execute(query, (user_name,)).fetchone()
            if result:
                news_setup = {'date_from': result[0],
                              'sort_by': result[1],
                              'topic_lang': result[2],
                              'news_lang': result[3],
                              'headlines_lang': result[4]}

        return news_setup if news_setup else self.default_news_setup()

    def update_arxiv_setup(self, username, arxiv_setup):
        with sqlite3.connect(self.user_data_db_path) as db:
            cursor = db.cursor()
            query = 'SELECT id FROM users WHERE user_name = (?)'
            result = cursor.execute(query, (username,)).fetchone()
            assert result, f'There is no record in table `users` for user {username}!'
            user_id = result[0]
            query = 'SELECT id FROM arxiv_setup WHERE user_id = (?)'
            result = cursor.execute(query, (user_id,)).fetchone()
            if result:
                query = '''UPDATE arxiv_setup 
                           SET sort_by = (?),
                               sort_order = (?),
                               max_results = (?),
                               topic_lang = (?),
                               results_lang = (?)
                           WHERE user_id = (?)'''
            else:
                query = '''INSERT INTO arxiv_setup(sort_by, sort_order, max_results, topic_lang, results_lang, user_id)
                           VALUES(?, ?, ?, ?, ?, ?)'''

            cursor.execute(query, (arxiv_setup['sort_by'], arxiv_setup['sort_order'], arxiv_setup['max_results'],
                                   arxiv_setup['topic_lang'], arxiv_setup['results_lang'], user_id))

    def get_arxiv_setup(self, user_name):
        """
        Returns user's arxiv setup dictionary from db if it exists,
        else returns default arxiv setup.
        :param user_name: Username in telegram
        :return: User's news setup dictionary
        """
        arxiv_setup = dict()
        with sqlite3.connect(self.user_data_db_path) as db:
            cursor = db.cursor()
            query = '''SELECT sort_by, sort_order, max_results, topic_lang,  results_lang
                       FROM arxiv_setup ars
                       LEFT JOIN users u on u.id = ars.user_id
                       WHERE u.user_name = (?)'''
            result = cursor.execute(query, (user_name,)).fetchone()
            if result:
                arxiv_setup = {'sort_by': result[0],
                               'sort_order': result[1],
                               'max_results': result[2],
                               'topic_lang': result[3],
                               'results_lang': result[4]}

        return arxiv_setup if arxiv_setup else self.default_arxiv_setup()
