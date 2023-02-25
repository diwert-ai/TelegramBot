from utils import gen_magic_string, get_bulls_cows_reply, is_numeric
from utils import run_google_ngrams_query,  top_k_ngrams, get_news


def on_start_command(update, context):
    print('Start event message received!')
    print(f'update: {update}')
    update.message.reply_text(f'Hi, {update.message.chat.username}!')


def on_guess_command(update, context):
    print('Guess event message received!')
    print(f'update: {update}')
    print(f'context.user_data: {context.user_data}')
    if 'magic' not in context.user_data:
        context.user_data['magic'] = gen_magic_string()
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
            del context.user_data['magic']
            message += ' Guessed right! 👍'

    else:
        message = 'Enter string of 4 digits!'
    update.message.reply_text(message)


def on_ngram_command(update, context):
    print('Ngram event message received!')
    args = context.args
    print(f'args: {args}')
    if args:
        user_string = args[0]
        print(f'user_string: {user_string}')
        stat = run_google_ngrams_query(user_string)
    else:
        stat = None

    update.message.reply_text(f'{stat}')


def on_decode_command(update, context):
    print('Ngram event message received!')
    args = context.args
    print(f'args: {args}')
    if args and is_numeric(user_string := args[0]) and ('0' not in user_string) and ('1' not in user_string):
        print(f'user_string: {user_string}')
        message = ', '.join(ngram[0] for ngram in top_k_ngrams(user_string))
    else:
        message = 'Code must be numeric without `0` and `1` characters!'

    update.message.reply_text(message)


def on_news_command(update, context):
    print('Ngram event message received!')
    args = context.args
    print(f'args: {args}')
    if args:
        user_string = ' '.join(args)
        print(f'user_string: {user_string}')
        message = get_news(user_string)
    else:
        message = 'Enter topic: /news [topic]!'

    update.message.reply_text(message, parse_mode='html')


def on_text_message(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)
