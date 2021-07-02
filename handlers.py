from glob import glob
from random import choice, randint
from datetime import datetime, timedelta
from utils import get_smile, play_random_numbers, main_keyboard

import ephem
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU')

def greet_user(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f"Здравствуй, пользователь {context.user_data['emoji']}!",
        reply_markup = main_keyboard()
    )

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    username = update.effective_user.first_name
    text = update.message.text
    update.message.reply_text(f"Здравствуй, {username} {context.user_data['emoji']}! Ты написал: {text}", reply_markup = main_keyboard())

def send_cat_picture(update, context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_filename,'rb'), reply_markup = main_keyboard())

def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message, reply_markup = main_keyboard())

def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
        reply_markup = main_keyboard()
    )

def planet(update, context):
    print('Вызвана /planet')  
    text_planet = update.message.text # объект update в нем атрибут message и взяли там текст
    planet_name = list(text_planet.split())[1] #получить имя планеты с помощью split
    today_date = datetime.now() #получить сегодняшнюю дату с помощью datetime
    # getattr(ephem, planet_name) - функция возвращает атрибут planet_name из коробки ephem == ephem.Mars
    # getattr(ephem, planet_name)(today_date)
    try:
        planet = getattr(ephem, planet_name)(today_date)
        const = ephem.constellation(planet)
    except:
        const = 'Попробуй еще раз'
    update.message.reply_text(const, reply_markup = main_keyboard())
