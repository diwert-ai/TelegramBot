import logging
from telegram.ext import Updater, CommandHandler
from config import Config

logging.basicConfig(filename='bot.log',
                    format='[%(asctime)s] [%(levelname)s] => %(message)s',
                    level=logging.INFO)


def on_start_command(update, context):
    print('Start event message received!')
    print(f'update: {update}')
    update.message.reply_text(f'Hi, {update.message.chat.username}!')


def main():
    bot = Updater(token=Config.token)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', on_start_command))

    logging.info('Bot run')
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
