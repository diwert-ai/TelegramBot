from random import choice
from string import digits
from requests import get
from urllib import parse


def is_numeric(string):
    for char in string:
        if char not in digits:
            return False
    return True


def get_bulls_cows_reply(user_string, magic_string):
    bulls, cows = sum([user_string[i] == magic_string[i] for i in range(4)]), 0
    for i, u_char in enumerate(user_string):
        if u_char in magic_string and magic_string[i] != user_string[i]:
            cows += 1

    return f'{bulls}B{cows}C'


def gen_magic_string():
    return ''.join([choice(digits) for _ in range(4)])


# https://www.geeksforgeeks.org/scrape-google-ngram-viewer-using-python/
def run_query(query, start_year=2000,
              end_year=2019, corpus=26,
              smoothing=0):
    # converting a regular string to
    # the standard URL format
    # eg: "geeks for,geeks" will
    # convert to "geeks%20for%2Cgeeks"
    query = parse.quote(query)

    # creating the URL
    url = 'https://books.google.com/ngrams/json?content=' + query + \
          '&year_start=' + str(start_year) + '&year_end=' + \
          str(end_year) + '&corpus=' + str(corpus) + '&smoothing=' + \
          str(smoothing) + ''

    # requesting data from the above url
    response = get(url)

    # extracting the json data from the response we got
    output = response.json()

    # creating a list to store the ngram data
    return_data = []

    if len(output) == 0:
        # if no data returned from site,
        # print the following statement
        return "No data available for this Ngram."
    else:
        # if data returned from site,
        # store the data in return_data list
        for num in range(len(output)):
            # getting the name
            return_data.append((output[num]['ngram'],

                                # getting ngram data
                                output[num]['timeseries'])
                               )

    return return_data
