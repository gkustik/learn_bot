from glob import glob
import logging
import ephem
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU')

from datetime import datetime, timedelta
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import choice, randint
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text("Здравствуй, пользователь!")

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def planet(update, context):
    print('Вызвана /planet')  
    text_planet = update.message.text
    planet_name = list(text_planet.split())[1] #получить имя планеты с помощью split
    today_date = datetime.now() #получить сегодняшнюю дату с помощью datetime
    if planet_name == 'Mars': #ввели корректно Марс, то
        planet = ephem.Mars(today_date)
        const = ephem.constellation(planet)
    elif planet_name == 'Mercury':
        planet = ephem.Mercury(today_date)
        const = ephem.constellation(planet)
    elif planet_name == 'Venus':
        planet = ephem.Mercury(today_date)
        const = ephem.constellation(planet)
    elif planet_name == 'Jupiter':
        planet = ephem.Jupiter(today_date)
        const = ephem.constellation(planet)
    elif planet_name == 'Saturn':
        planet = ephem.Saturn(today_date)
        const = ephem.constellation(planet)
    elif planet_name == 'Uranus':
        planet = ephem.Uranus(today_date)
        const = ephem.constellation(planet)
    elif planet_name == 'Neptune':
        planet = ephem.Neptune(today_date)
        const = ephem.constellation(planet)
    elif planet_name == 'Pluto':
        planet = ephem.Pluto(today_date)
        const = ephem.constellation(planet)
    else:
        const = 'Попробуй еще раз'
    update.message.reply_text(const)


def play_random_numbers(user_number):
    bot_number = randint(user_number -10, user_number +10)
    if user_number > bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!"
    elif user_number == bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ничья!"
    else:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, я выиграл!"
    return message

def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            # message = f"Ваше число {user_number}" заменяем на игру бота в цифры
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message)

def send_cat_picture(update, context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    print(cat_pic_filename)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(CommandHandler('planet', planet))
    
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()