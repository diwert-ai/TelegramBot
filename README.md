# TelegramBot Project
A project task from a python course (HSE DPO program).

## Install
1. Clone repo from GitHub to project folder: `git clone https://github.com/diwert-ai/TelegramBot [project-folder]`
2. Make virtual environment (with interpreter python 3.10) in project folder (see help here https://docs.python.org/3.10/library/venv.html)
3. Install requirements (in virtual environment): `pip install -r requirements.txt`
4. Make file `config.py` in project folder
5. Write to the `config.py`:
```
class Config:
    token = 'bot key received at registration'
```
6. Run bot (in virtual environment): `python bot.py`

## Bot commands
1. `/start` - The bot responds with a greeting, using the username.
2. `/g [4-digits string - user's guess]` - Bot plays a game of bulls and cows. The bot guesses a four-digit number and returns
the number of bulls and cows according to the user's guess in the format nBmC, where n is the number of bulls and m is
the number of cows.
3. `/ng [n-gram]` - Bot returns n-gram statistics requested from Google Ngram Viewer service.