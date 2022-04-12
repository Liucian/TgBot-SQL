import random
import telebot
import Dbase
from telebot import types

memory = {}
memory_progress = {}

token = '5210752394:AAEGzzEzH2UmNJk_pLFjcCtXno3e6zWUZ5w'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['help', 'start'])
def wlcm_send(message):
    keyboard = types.InlineKeyboardMarkup()
    key_start = types.InlineKeyboardButton(text='Начать', callback_data='yes')
    key_stop = types.InlineKeyboardButton(text='Стоп', callback_data='no')
    keyboard.add(key_start)
    keyboard.add(key_stop)
    bot.reply_to(message, "Приветствую тебя! \n Я бот-игра суть которой состоит в угадывании чисел в диапазоне 0-1 "
                          "\n Если ты угадаешь я тебе запишу один балл в другом случае сниму "
                          "\n Для начала игры нажми кнопку (Начать) !)", reply_markup=keyboard)
    Dbase.print_db()
    Dbase.saveScore()


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global memory
    global memory_progress
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Введи число:")
        memory[call.from_user.id] = True
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Хорошо,поиграем в другой раз((")
    elif call.data == "again":
        bot.send_message(call.message.chat.id, "Введи число:")
        memory[call.from_user.id] = True
    elif call.data == "back":
        memory[call.from_user.id] = False
        bot.send_message(call.message.chat.id, "Спасибо за игру!>")
    elif call.data == "score":
        bot.send_message(call.message.chat.id, "Ваши очки:" + str(memory_progress[call.from_user.id]))


@bot.message_handler(content_types=['text'])
def rand1(message):
    if memory[message.from_user.id]:
        num = random.randint(0, 1)
        bot.send_message(message.chat.id, text="Я загадал цифру:" + str(num))
        keyboard = types.InlineKeyboardMarkup()
        key_again = types.InlineKeyboardButton(text='Заново', callback_data='again')
        key_stop2 = types.InlineKeyboardButton(text='Завершить игру', callback_data='back')
        key_score1 = types.InlineKeyboardButton(text='Узнать свой счёт', callback_data='score')
        keyboard.add(key_score1)
        keyboard.add(key_again)

        keyboard.add(key_stop2)
        if memory_progress.get(message.from_user.id) is None:
            memory_progress[message.from_user.id] = 0
        if message.text == str(num):
            bot.send_message(message.chat.id, text="Ты угадал!", reply_markup=keyboard)
            memory_progress[message.from_user.id] += 1
        else:
            bot.send_message(message.chat.id, text="Ты не угадал,попробуй ещё!", reply_markup=keyboard)
            memory_progress[message.from_user.id] -= 1


bot.polling(non_stop=True)
