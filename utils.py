from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.utils.request import Request
from random import choice, randint

import settings

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI) 
        return emojize(smile, use_aliases=True)
    return user_data['emoji']

def play_random_numbers(user_number):
    bot_number = randint(user_number -10, user_number +10)
    if user_number > bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!"
    elif user_number == bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ничья!"
    else:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, я выиграл!"
    return message

def main_keyboard(): # такое написание функции означает, что она ничего не принимает
    return ReplyKeyboardMarkup([['Прислать котика', 'Тест', KeyboardButton('Мои координаты', request_location = True)]], resize_keyboard=True)

