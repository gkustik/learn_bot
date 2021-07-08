from glob import glob
import os
import ephem
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU')
from random import choice
from datetime import datetime, timedelta
from db import db, get_or_create_user

from utils import is_cat, main_keyboard, play_random_numbers


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


def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    print("Вызван /start")
    update.message.reply_text(
        f"Здравствуй, пользователь {user['emoji']}!",
        reply_markup=main_keyboard()
    )

def talk_to_me(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    text = update.message.text
    print(text)
    update.message.reply_text(f"{text} {user['emoji']}", reply_markup=main_keyboard())

def guess_number(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message, reply_markup=main_keyboard())

def send_cat_picture(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    cat_photo_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'), reply_markup=main_keyboard())

def user_coordinates(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {user['emoji']}!",
        reply_markup=main_keyboard()
    )

def check_user_photo(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text("Обрабатываем фотографию")
    os.makedirs("downloads", exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join("downloads", f"{user_photo.file_id}.jpg")
    user_photo.download(file_name)
    if is_cat(file_name):
        update.message.reply_text("Обнаружен котик, добавляю в библиотеку")
        new_filename = os.path.join("images", f"cat_{user_photo.file_id}.jpg")
        os.rename(file_name, new_filename)
    else:
        update.message.reply_text("Тревога, котик на фото не обнаружен")
        os.remove(file_name)