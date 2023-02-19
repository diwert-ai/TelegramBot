from utils import gen_magic_string, get_bulls_cows_reply, is_numeric


def on_start_command(update, context):
    print('Start event message received!')
    print(f'update: {update}')
    update.message.reply_text(f'Hi, {update.message.chat.username}!')


def on_guess_command(update, context):
    print('Guess event message received!')
    print(f'update: {update}')
    if 'magic' not in context.user_data:
        magic_string = gen_magic_string()
        context.user_data['magic'] = magic_string
    else:
        magic_string = context.user_data['magic']
    print(f'magic number: {magic_string}')
    args = context.args
    print(f'context.args: {args}')
    if args and len(args[0]) == 4 and is_numeric(args[0]):
        user_string = args[0]
        print(f'user_string: {user_string}, magic_string: {magic_string}')
        bulls_cows_reply = get_bulls_cows_reply(user_string, magic_string)
        message = f'{bulls_cows_reply}'
        if bulls_cows_reply[0] == '4':
            context.user_data['magic'] = gen_magic_string()
            message += ' Guessed right! The new string is guessed.'
    else:
        message = 'Enter string of 4 digits!'
    update.message.reply_text(message)


def on_text_message(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)
