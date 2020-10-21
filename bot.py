import telebot as tb
from telebot import types

import requests
from bs4 import BeautifulSoup as bs
from random import randint


def parse(num):
    img1 = []
    links_dict = {
        '1': 'https://unsplash.com/t/nature',
        '2': 'https://unsplash.com/t/interiors',
        '3': 'https://unsplash.com/t/street-photography'
    }
    session = requests.Session()
    request = session.get(links_dict[num])
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        imgs = soup.find_all('img', class_='_2VWD4 _2zEKz')
        for img in imgs:
            img1.append(img.get('src'))
    return img1[randint(0, len(img1))]


bot = tb.TeleBot('796324726:AAFu7JnYj1kD_2ZvK-3luUzc_b2_FA33vDY')


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Картинка')
    markup.add(item1)
    bot.send_message(message.chat.id, f'Добро пожаловать', parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def response(message):
    if message.chat.type == 'private':
        if message.text == 'Картинка':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('1', callback_data='1')
            item2 = types.InlineKeyboardButton('2', callback_data='2')
            item3 = types.InlineKeyboardButton('3', callback_data='3')
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, 'Choice picture', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == '1':
                bot.send_photo(call.message.chat.id, parse('1'))
            elif call.data == '2':
                bot.send_photo(call.message.chat.id, parse('2'))
            elif call.data == '3':
                bot.send_photo(call.message.chat.id, parse('3'))
    except Exception as e:
        print(repr(e))


bot.polling()
