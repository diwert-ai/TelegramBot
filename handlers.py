from utils import gen_magic_string, get_bulls_cows_reply, is_numeric
from utils import run_google_ngrams_query, top_k_ngrams, get_news
from utils import get_arxiv_info, get_translated_text, db_register_user


def on_start_command(update, context):
    print('Start event message received!')
    print(f'update: {update}')
    chat = update.message.chat
    user_data = {'user_name': chat.username,
                 'first_name': chat.first_name,
                 'last_name': chat.last_name}
    status = db_register_user(user_data)
    print(f'register status: {status}')
    if status:
        message = f'Long time no see! Hi, {chat.username}! 🤝'
    else:
        message = f'Sounds like this is your first time here! 🙂 Welcome, {chat.username}! 😉'

    update.message.reply_text(message)


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
    print('Decode event message received!')
    args = context.args
    print(f'args: {args}')
    if args and is_numeric(user_string := args[0]) and ('0' not in user_string) and ('1' not in user_string):
        print(f'user_string: {user_string}')
        message = ', '.join(ngram[0] for ngram in top_k_ngrams(user_string))
    else:
        message = 'Code must be numeric without `0` and `1` characters!'

    update.message.reply_text(message)


def on_news_command(update, context):
    print('News event message received!')
    args = context.args
    print(f'args: {args}')
    if args:
        user_string = ' '.join(args)
        print(f'user_string: {user_string}')
        message = get_news(user_string)
    else:
        message = 'Enter topic: /news [topic]!'

    update.message.reply_text(message, parse_mode='html')


def on_arxiv_command(update, context):
    print('Arxiv event message received!')
    args = context.args
    print(f'args: {args}')
    if args:
        user_string = ' '.join(args)
        print(f'user_string: {user_string}')
        message = get_arxiv_info(user_string)
    else:
        message = 'Enter topic: /arxiv [topic]!'

    '''msgs = [message[i:i + 4096] for i in range(0, len(message), 4096)]
    for text in msgs:
        update.message.reply_text(text, parse_mode='html')'''

    update.message.reply_text(message, parse_mode='html')


def on_echo_command(update, context):
    print('Echo event message received!')
    args = context.args
    print(f'args: {args}')
    if args:
        user_string = ' '.join(args)
        print(f'user_string: {user_string}')
        message = user_string
    else:
        message = 'Enter text please!'
    update.message.reply_text(message)


def on_trans_command(update, context):
    print('Trans event message received!')
    args = context.args
    print(f'args: {args}')
    if args:
        user_string = ' '.join(args)
        print(f'user_string: {user_string}')
        message = get_translated_text(user_string)
    else:
        message = 'Enter text to translate!'

    update.message.reply_text(message)


def do_translation(update, context):
    print('Text message received!')
    message = get_translated_text(update.message.text)
    update.message.reply_text(message)
