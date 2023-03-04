from random import choice
from string import digits


class BullsAndCowsEngine:
    def __init__(self):
        pass

    @staticmethod
    def get_bulls_and_cows(user_string, magic_string):
        bulls, cows = sum([user_string[i] == magic_string[i] for i in range(4)]), 0
        for i, u_char in enumerate(user_string):
            if u_char in magic_string and magic_string[i] != user_string[i]:
                cows += 1

        return f'{bulls}B{cows}C'

    @staticmethod
    def new_guess():
        return ''.join([choice(digits) for _ in range(4)])
