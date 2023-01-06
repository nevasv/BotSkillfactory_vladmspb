# bot из задания 5.1 . Введение

"""
Бот принимае соощения /start /help, отвечает на отправленную фотографию и звук
Создан по материалам задания 5.1 . Введение

"""
import telebot
from bot.config import TOKEN

bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Привет пришелец, {message.chat.username}")


# Обрабатываются все сообщения, содержащие команды voice.
@bot.message_handler(content_types=["voice", ])
def repeat(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Большой брат пишет, говори ещё ))")


# Обрабатываются все сообщения, содержащие команды photo.
@bot.message_handler(content_types=['photo', ])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Nice meme XDD')


# Запуск полинга
bot.polling(none_stop=True)
