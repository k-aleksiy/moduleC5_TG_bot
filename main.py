import telebot
from telebot import types

from config import TOKEN, keys
from extensions import APIExcepshion, Convertor


def cr_markup(base=None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in keys.keys():
        if val != base:
            buttons.append(types.KeyboardButton(val.capitalize()))
    markup.add(*buttons)
    return markup

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Здравствуйте!!! Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты, цену которой хотите узнать> \
\n<имя валюты, в которой хотите узнать цену первой валюты>  \
\n<количество переводимой валюты>\
\nУвидеть список всех доступных валют: /values\
\nПриструпить к конвертации: /convert'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные варианты валют:'
    for a in keys.keys():
        text = '\n'.join((text, a))
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберите валюту, из которой конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=cr_markup())
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = 'Выберите валюту, в которую конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=cr_markup(base))
    bot.register_next_step_handler(message, quote_handler, base)

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip().lower()
    text = 'Введите количество конвертируемой валюты:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)

def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        new_price = Convertor.get_price(base, quote, amount)
    except APIExcepshion as e:
        bot.reply_to(message, f"Ошибка пользователя!\n{e}")
    else:
        text = f"{new_price}"
        bot.send_message(message.chat.id, text)


bot.polling()