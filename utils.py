from random import randint


def get_bulls_cows_reply(user_number, magic_number):
    u_str, m_str, cows = str(user_number), str(magic_number), 0
    bulls = sum([u_str[i] == m_str[i] for i in range(4)])
    for i, uchar in enumerate(u_str):
        if uchar in m_str and m_str[i] != u_str[i]:
            cows += 1

    return f'{bulls}B{cows}C'


def gen_magic_number():
    magic_number = 0
    for k in (1, 10, 100, 1000):
        magic_number += randint(1, 9) * k
    return magic_number
