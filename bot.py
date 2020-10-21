import telebot as tb
from telebot import types
import requests
from bs4 import BeautifulSoup


def parse(img):
    url = 'https://unsplash.com/photos/' + img
    r = requests.get(url).text
    content = BeautifulSoup(r, 'html.parser')

    img_news = content.find('img').get('src')


bot = tb.TeleBot('')
link = 'https://unsplash.com/photos/'


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
                bot.send_message(call.message.chat.id, link + 'nSy8T8Oxrcs')
                bot.send_photo(call.message.chat.id, parse('PJ61QqdVWMY'))
            elif call.data == '2':
                bot.send_message(call.message.chat.id, link + 'Iy9h7vTRUpo')
                bot.send_photo(call.message.chat.id, parse('PJ61QqdVWMY'))
            elif call.data == '3':
                bot.send_message(call.message.chat.id, link + 'PJ61QqdVWMY')
                bot.send_photo(call.message.chat.id, parse('PJ61QqdVWMY'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Как дела?',
                                  reply_markup=None)
    except Exception as e:
        print(repr(e))


bot.polling()
