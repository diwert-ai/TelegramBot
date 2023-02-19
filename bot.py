import logging
from random import randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import Config

logging.basicConfig(filename='bot.log',
                    format='[%(asctime)s] [%(levelname)s] => %(message)s',
                    level=logging.INFO)


def on_start_command(update, context):
    print('Start event message received!')
    print(f'update: {update}')
    update.message.reply_text(f'Hi, {update.message.chat.username}!')


def get_bulls_cows_reply(user_number, magic_number):
    ustr, mstr, cows = str(user_number), str(magic_number), 0
    bulls = sum([ustr[i] == mstr[i] for i in range(4)])
    for i, uchar in enumerate(ustr):
        if uchar in mstr and mstr[i] != ustr[i]:
            cows += 1

    return f'{bulls}B{cows}C'


def gen_magic_number():
    magic_number = 0
    for k in (1, 10, 100, 1000):
        magic_number += randint(1, 9) * k
    return magic_number


def on_guess_command(update, context):
    print('Guess event message received!')
    print(f'update: {update}')
    if 'magic' not in context.user_data:
        magic_number = gen_magic_number()
        context.user_data['magic'] = magic_number
    else:
        magic_number = context.user_data['magic']
    print(f'magic number: {magic_number}')
    args = context.args
    print(f'context.args: {args} {(len(args[0]), args[0][0]) if args else None}')
    if args and len(args[0]) == 4 and args[0][0] != '0':
        try:
            user_number = int(args[0])
            print(f'user_number: {user_number}, magic_number: {magic_number}')
            message = f'{get_bulls_cows_reply(user_number, magic_number)}'
        except (TypeError, ValueError):
            message = 'Not a integer!'
    else:
        message = 'Enter 4-digit integer!'
    update.message.reply_text(message)


def on_text_message(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)


def main():
    bot = Updater(token=Config.token)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', on_start_command))
    dp.add_handler(CommandHandler('g', on_guess_command))
    dp.add_handler(MessageHandler(Filters.text, on_text_message))

    logging.info('Bot run')
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
