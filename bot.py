from telegram.ext import Updater, CommandHandler
from config import Config


def on_start_command(update, context):
    print('Start event message received!')


def main():
    bot = Updater(token=Config.token)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', on_start_command))

    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
