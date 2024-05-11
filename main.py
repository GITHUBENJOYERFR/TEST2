from telebot import types
import telebot
from telebot import time
from mozq import *
bot = telebot.TeleBot(token='6346702040:AAEMIhb63Mbzy5RXNElvN0X3l_tT93tmjCY')

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    bot.send_message(user_id,'здрасте,я тестовый бот!''\n /help - кнопка меню')

@bot.message_handler(commands=['help'])
def help(message):
    user_id = message.chat.id
    help_text = 'нажмите на нужную кнопку'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton('информация про отели:')
    button2 = types.KeyboardButton('посмотреть билеты:')
    button3 = types.KeyboardButton('контакты по отелям')


    markup.row(button1)
    markup.row(button2, button3)
    bot.send_message(user_id,help_text,reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def text_message_handler(message):
    user_id = message.chat.id
    text = message.text.lower()

    if text == 'контакты по отелям':
        bot.send_message(user_id,contacts)




bot.polling(none_stop=True)


