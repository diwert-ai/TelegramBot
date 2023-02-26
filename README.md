# TelegramBot Project
A project task from a python course (HSE DPO program).

## Install
1. Clone repo from GitHub to project folder: `git clone https://github.com/diwert-ai/TelegramBot [project-folder]`
2. Make virtual environment (with interpreter python 3.10) in project folder (see help here https://docs.python.org/3.10/library/venv.html)
3. Install requirements (in virtual environment): `pip install -r requirements.txt`
4. Create sqllite database for ngrams storing with table:
```
CREATE TABLE ngrams (
    id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    ngram TEXT (256) UNIQUE
                     NOT NULL,
    prob  REAL       NOT NULL
                     DEFAULT (0.0) 
);
```
5. Make file `config.py` in project folder
6. Write to the `config.py`:
```
class Config:
    telegram_bot_token = 'bot key received at registration'
    ngrams_db_path = 'path to sqllite for ngrams storing'
    news_api_key = 'api key for newsapi.org service'
```
7. Run bot (in virtual environment): `python bot.py`

## Bot commands
1. `/start` - The bot responds with a greeting, using the username.
2. `/g [4-digits string - user's guess]` - Bot plays a game of bulls and cows. The bot guesses a four-digit number and returns
the number of bulls and cows according to the user's guess in the format nBmC, where n is the number of bulls and m is
the number of cows.
3. `/ngram [n-gram]` - Bot returns n-gram statistics requested from Google Ngram Viewer service.
4. `/decode [numeric code]` - The bot returns the most likely decoding of the number string.
Each digit is recoded according to the rules of the keypad of a pushbutton phone.
5.  `/news [topic]` - The bot returns the top 5 news items with a given topic, using the service https://newsapi.org
6. `/arxiv [topic]` - The bot returns the last 5 articles with the given topic, published on https://arxiv.org
7. `/trans [phrase]` - The bot returns the translation of the phrase from Russian to English