from utils import gen_magic_number, get_bulls_cows_reply


def on_start_command(update, context):
    print('Start event message received!')
    print(f'update: {update}')
    update.message.reply_text(f'Hi, {update.message.chat.username}!')


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
            bulls_cows_reply = get_bulls_cows_reply(user_number, magic_number)
            message = f'{bulls_cows_reply}'
            if bulls_cows_reply[0] == '4':
                context.user_data['magic'] = gen_magic_number()
                message += ' Guessed right! The new number is guessed.'

        except (TypeError, ValueError):
            message = 'Not a integer!'
    else:
        message = 'Enter 4-digit integer!'
    update.message.reply_text(message)


def on_text_message(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)
