# TelegramBot Project
A project task from a python course (HSE DPO program).

## Install
1. Clone repo from GitHub to project folder: `git clone https://github.com/diwert-ai/TelegramBot [project-folder]`
2. Make virtual environment (with interpreter python 3.10) in project folder (see help here https://docs.python.org/3.10/library/venv.html)
3. Install requirements (in virtual environment): `pip install -r requirements.txt`
4. Create sqlite database `ngrams.db` for ngrams storing with table `ngrams` :
```
CREATE TABLE ngrams (
    id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    ngram TEXT (256) UNIQUE
                     NOT NULL,
    prob  REAL       NOT NULL
                     DEFAULT (0.0) 
);
```
5. Create sqlite database `user_data.db` for storing user data with table `users`:
```
CREATE TABLE users (
    id         INTEGER    PRIMARY KEY AUTOINCREMENT,
    user_name  TEXT (128) NOT NULL
                          UNIQUE,
    first_name TEXT (128),
    last_name  TEXT (128),
    reg_date              NOT NULL
                          DEFAULT ( (DATETIME('now') ) ) 
);
```
with table `news_setup`:
```
CREATE TABLE news_setup (
    id             INTEGER   PRIMARY KEY AUTOINCREMENT,
    user_id        INTEGER   REFERENCES users (id) ON DELETE CASCADE
                             NOT NULL,
    sort_by        TEXT (64) NOT NULL
                             DEFAULT ('relevancy'),
    news_lang      TEXT (8)  DEFAULT ('en'),
    topic_lang     TEXT (8)  NOT NULL
                             DEFAULT ('en'),
    headlines_lang TEXT (8)  NOT NULL
                             DEFAULT ('ru'),
    date_from                NOT NULL
                             DEFAULT ( (DATETIME('now') ) ) 
);
```
and with table `arxiv_setup`
```
CREATE TABLE arxiv_setup (
    id           INTEGER   PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER   REFERENCES users (id) ON DELETE CASCADE
                           NOT NULL,
    sort_by      TEXT (64) NOT NULL
                           DEFAULT ('relevance'),
    sort_order   TEXT (64) NOT NULL
                           DEFAULT ('descending'),
    max_results  INTEGER   NOT NULL
                           DEFAULT (5),
    topic_lang   TEXT (8)  NOT NULL
                           DEFAULT ('en'),
    results_lang TEXT (8)  NOT NULL
                           DEFAULT ('ru') 
);
```
6. Make file `config.py` in project folder
7. Write to the `config.py`:
```
class Config:
    telegram_bot_token = 'bot key received at registration'
    ngrams_db_path = 'path to sqlite db for ngrams storing'
    user_data_db_path = 'path to sqlite db for user data storing'
    news_api_key = 'api key for newsapi.org service'
```
8. Run bot (in virtual environment): `python bot.py`

## Bot commands
1. `/help` - The bot show list of commands
2. `/start` - The bot responds with a greeting, using the username. It finds out if the user has been there before and 
if not, it registers this user in the sqlite database. A menu appears with two buttons:
`news setup` and `arxiv setup`. The first launches the conversation to create user parameters for requests 
to https://newsapi.org (used in the `/news` and `/gnews` commands). The second one is analyzed for queries
to https://arxiv.org. User parameters are stored in `context.user_data` and stored in the sqlite database.
3. `/g [4-digits string - user's guess]` or `/guess` - Bot plays a game of bulls and cows. The bot guesses a four-digit
number and returns
the number of bulls and cows according to the user's guess in the format nBmC, where n is the number of bulls and m is
the number of cows.
4. `/ngram [n-gram]` - Bot returns n-gram statistics requested from Google Ngram Viewer service.
5. `/decode [numeric code]` - The bot returns the most likely decoding of the number string.
Each digit is recoded according to the rules of the keypad of a pushbutton phone. The probability is determined by
the n-gram statistics obtained from the Google Ngram Viewer service. The n-gram stats are saved in a sqlite database,
which allows you to take the stats from the database instead of making the same queries to the Google Ngram Viewer.
6. `/news [topic]` - The bot returns the top 5 news items with a given topic, using the service https://newsapi.org
with the parameters that have been configured in `news setup` conversation
7. `/gnews [topic]` - The bot does the same thing as the `/news` command, but a menu appears with the commands
`next 5 news` (gives the next 5 news from the general pool that the https://newsapi.org service has returned) and
`return setup` (returns the `news setup` and `arxiv setup` menu buttons - see step 1). Showing news on the button
`next 5 news` is looped to an endless loop, ie, after the last news from the pool will be shown, the show will again
start with the first news.
8. `/arxiv [topic]` - The bot returns the last 5 articles (by submitted date) with the given topic, published 
on https://arxiv.org with the parameters that have been configured in `arxiv setup` conversation
9. `/garxiv [topic]` - The bot does the same thing as the `/arxiv` command, but a menu appears with the commands
`next 5 articles` (gives the next 5 articles from the general pool that the https://arxiv.org service has returned) and
`return setup` (returns the `news setup` and `arxiv setup` menu buttons - see step 1). Showing articles on the button
`next 5 articles` is looped to an endless loop, ie, after the last article from the pool will be shown, the show will 
again start with the first article.
10. `/trans [phrase]` - The bot returns the translation of the phrase from Russian to English
11. `/echo [text]` - The bot just reply with an echo text