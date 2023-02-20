# TelegramBot Project
A project task from a python course (HSE DPO program).

## Install
1. Clone repo from GitHub to project folder: `git clone https://github.com/diwert-ai/TelegramBot [project-folder]`
2. Make virtual environment (with interpreter python 3.10) in project folder (see help here https://docs.python.org/3/library/venv.html)
3. Install requirements (in virtual environment): `pip install -r requirements.txt`
4. Make file `config.py` in project folder
5. Write to the `config.py`:
```
class Config:
    token = 'bot key received at registration'
```
6. Run bot (in virtual environment): `python bot.py`