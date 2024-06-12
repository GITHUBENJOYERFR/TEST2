from telebot import types
import telebot
from mozg import parser
import datetime

bot = telebot.TeleBot(token='6346702040:AAEMIhb63Mbzy5RXNElvN0X3l_tT93tmjCY')
data_users = []

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    bot.send_message(user_id, 'Добро пожаловать в тур агентство "Semey-fly"'
                     + '\n /help - кнопка меню')

@bot.message_handler(commands=['help'])
def help(message):
    user_id = message.chat.id
    help_text = "Выберите действие:"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton('Получить информацию про отели')
    button2 = types.KeyboardButton('Посмотреть билеты')
    button3 = types.KeyboardButton('Контакты нашей компании')

    markup.row(button1)
    markup.row(button2, button3)
    bot.send_message(user_id, help_text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def text_message_handler(message):
    user_id = message.chat.id
    text = message.text.lower()

    if text == 'контакты нашей компании':
        bot.send_message(user_id, 'Ваши контакты...')
    elif text == 'получить информацию про отели':
        bot.send_message(user_id, 'Введите город:')
        bot.register_next_step_handler(message, city)

def city(message):
    user_id = message.chat.id
    gorod = message.text
    data_users.append(gorod)
    bot.send_message(user_id, 'Введите даты когда хотите заселиться в отель:\nК примеру 23.05.2024')
    bot.register_next_step_handler(message, data_start)

def data_start(message):
    print("запускается функция data start")
    user_id = message.chat.id
    starts_date = message.text
    try:
        starts_date = datetime.datetime.strptime(starts_date, "%d.%m.%Y")
        if starts_date >= datetime.datetime.now():
            data_users.append(starts_date)
            bot.send_message(user_id, 'Введите дату выселения в том же формате')
            bot.register_next_step_handler(message, finish_date)
        else:
            bot.send_message(user_id, 'Дата заселения не может быть в прошлом. Введите заново.')
            bot.register_next_step_handler(message, data_start)
    except ValueError:
        bot.send_message(user_id, 'Неправильный формат даты. Попробуйте еще раз.')
        bot.register_next_step_handler(message, data_start)

def finish_date(message):
    print("запускается функция finish date")
    user_id = message.chat.id
    finish_date_text = message.text
    try:
        finish_date = datetime.datetime.strptime(finish_date_text, "%d.%m.%Y")
        if finish_date > data_users[1]:
            data_users.append(finish_date)
            bot.send_message(user_id, 'Ожидайте результатов поиска по нашим базам')
            send_result(message)
        else:
            bot.send_message(user_id, 'Дата выселения должна быть позже даты заселения. Попробуйте еще раз.')
            bot.register_next_step_handler(message, finish_date)
    except ValueError:
        bot.send_message(user_id, 'Неправильный формат даты. Попробуйте еще раз.')
        bot.register_next_step_handler(message, finish_date)

def send_result(message):
    print('Запуск отправки результатов')
    user_id = message.chat.id
    city = data_users[0]
    start_date = data_users[1].strftime('%Y-%m-%d')
    end_date = data_users[2].strftime('%Y-%m-%d')
    print(f'Преобразованные даты: {start_date}, {end_date}')
    lst = parser(city, start_date, end_date)
    if lst:
        for hotels in lst:
            bot.send_message(user_id, f'Название отеля: {hotels[0]}\nЦена за период отдыха: {hotels[1]}')
    else:
        bot.send_message(user_id, 'Нет результатов для выбранных дат.')

bot.polling(none_stop=True)
