# bot
import telebot

TOKEN = "5635438312:AAHVu-3ToFXfVK1JuNYvz1KvzjUwdI3jfYs"

bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Привет пришелец, {message.chat.username}")


@bot.message_handler(content_types=["voice", ])
def repeat(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Большой брат пишет, говори ещё ))")


@bot.message_handler(content_types=['photo', ])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Nice meme XDD')


bot.polling(none_stop=True)