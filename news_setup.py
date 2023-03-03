from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from utils import setup_keyboard
from userdata_db import UserDataDB


def sort_up_keyboard():
    return ReplyKeyboardMarkup([['relevancy', 'popularity', 'publishedAt']], one_time_keyboard=True)


def news_lang_keyboard():
    return ReplyKeyboardMarkup([['ru', 'en', 'de', 'fr', 'it', 'es']], one_time_keyboard=True)


def topic_lang_keyboard():
    return ReplyKeyboardMarkup([['ru', 'en']], one_time_keyboard=True)


def headlines_lang_keyboard():
    return ReplyKeyboardMarkup([['ru', 'en']], one_time_keyboard=True)


def news_setup_start(update, context):
    update.message.reply_text("Welcome to news service settings!\n" +
                              "I'm going to ask you a few questions. - Pay attention!\n" +
                              "Let's go!")
    update.message.reply_text("1. Specify the date from which the news was published (format: yyyy-mm-dd)",
                              reply_markup=ReplyKeyboardRemove())
    return 'date_from'


def news_setup_date_from(update, context):
    date_from = update.message.text
    context.user_data['news_setup'] = {'date_from': date_from}
    update.message.reply_text('2. Select the order in which the news is sorted',
                              reply_markup=sort_up_keyboard())
    return 'sort_up'


def news_setup_sort_by(update, context):
    context.user_data['news_setup']['sort_by'] = update.message.text
    update.message.reply_text('3. Select a news language',
                              reply_markup=news_lang_keyboard())
    return 'news_lang'


def news_setup_news_lang(update, context):
    context.user_data['news_setup']['news_lang'] = update.message.text
    update.message.reply_text('4. Select the language in which you will formulate the topic of the news',
                              reply_markup=topic_lang_keyboard())
    return 'topic_lang'


def news_setup_topic_lang(update, context):
    context.user_data['news_setup']['topic_lang'] = update.message.text
    update.message.reply_text('5. Select the language in which you want to translate the headlines',
                              reply_markup=headlines_lang_keyboard())
    return 'headlines_lang'


def news_setup_headlines_lang(update, context):
    context.user_data['news_setup']['headlines_lang'] = update.message.text
    username = update.message.chat.username
    user_news_setup = context.user_data['news_setup']
    message = f"""Thanks! Your news setup:
<b>Date from</b>: {user_news_setup['date_from']}
<b>Sort by</b>: {user_news_setup['sort_by']}
<b>News language</b>: {user_news_setup['news_lang']}
<b>Topic language</b>: {user_news_setup['topic_lang']}
<b>Headlines language</b>: {user_news_setup['headlines_lang']}"""
    UserDataDB().update_news_setup(username, user_news_setup)
    update.message.reply_text(message, parse_mode='html', reply_markup=setup_keyboard())
    update.message.reply_text('News setup have stored to db!')
    return ConversationHandler.END


def news_setup_fallback(update, context):
    update.message.reply_text('Wrong input! Please do it again!')
