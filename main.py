import random
import sqlite3
import telebot
from telebot import types

TOKEN = 'your token'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Сделай идею')
        markup.add(btn1)
        bot.send_message(message.from_user.id, '❓ Выберите что-то из поля ниже', reply_markup=markup)
    elif message.text == 'Сделай идею':
        msg = bot.send_message(message.chat.id,
                               f"Сколько должно быть идей?-->Что возьмём за идею?(писать через пробел)\n!!если идея состоит из двух слов, писать через тире!!\n Пример: 10 итоговый-проект")
        bot.register_next_step_handler(msg, gen)


def gen(message):
    n, forinput = message.text.split()
    nInteger = int(n)
    conn = sqlite3.connect('bebra.db')
    cursor = conn.cursor()
    try:
        for i in range(nInteger):
            n1 = random.randint(0, 1008)
            n2 = random.randint(0, 1009)
            n3 = random.randint(0, 1009)
            bebra1 = cursor.execute(f"SELECT essential FROM generator WHERE rowid = ?", (n1,)).fetchone()
            bebra2 = cursor.execute(f"SELECT adjective FROM generator WHERE rowid = ?", (n2,)).fetchone()
            bebra3 = cursor.execute(f"SELECT verb FROM generator WHERE rowid = ?", (n3,)).fetchone()

            # Error handling for bebra1
            if bebra1:
                bebra1_value = bebra1[0]
            else:
                bebra1_value = "No essential found[ERROR]"

            # Error handling for bebra2
            if bebra2:
                bebra2_value = bebra2[0]
            else:
                bebra2_value = "No adjective found[ERROR]"

            # Error handling for bebra3
            if bebra3:
                bebra3_value = bebra3[0]
            else:
                bebra3_value = "No verb found[ERROR]"

            bot.send_message(message.chat.id, f'{forinput}➝ {bebra3_value}, {bebra2_value}, {bebra1_value}')
    finally:
        cursor.close()
        conn.close()


bot.polling(none_stop=True)


