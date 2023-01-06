# bot из задания 5.6 . Итоговый проект
# -*- coding: utf-8 -*-
from loguru import logger
import requests
import telebot
from lxml import etree
from bot.config import TOKEN

logger.add("logs/logs.log", format="{time} {level} {message}", level='DEBUG', rotation="20 KB", compression="zip")
# serialize=True and  "logs/logs.json"
# logger.debug('Error')
# logger.info('Information message')
# logger.warning('Warning')
# @logger.catch()


bot = telebot.TeleBot(TOKEN)

val_list = {
    '1': 'руб',
    '2': 'usd',
    '3': 'eur',
    '4': 'cny',
    '5': 'byn',
    '6': 'jpy'

}

task =[]

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Привет тестировщик, {message.chat.username} \n"
                                      f"Для начала узнайте номер валюты: список валют /currency \n"
                                      f"Дальше нужно вводить через пробел  \n"
                                      f"Шаг №1 <номер конвертируемой валюты> \n"
                                      f"Шаг №2 <номер валюты результата> \n"
                                      f"Шаг №3 <колличество конвертируемой валюты> \n")


# Обрабатываются команда /currency.
@bot.message_handler(commands=['currency'])
def handle_start_help(message: telebot.types.Message):
    text = 'Доступные валюты \n' \
           ' 1.Рубль  \n' \
           ' 2. Доллар США {}\n' \
           ' 3. Евро \n' \
           ' 4. Китайский юань \n' \
           ' 5. Беларусский рубль \n' \
           ' 6. Японская йена'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert_currency(message: telebot.types.Message):
    code1, code2, value = message.text.split(' ')
    global task
    task = [code1, code2 , value]
    text = f"Конвертировать {value} {val_list[code1]} в {val_list[code2]} !! посчитать сечас? /calculate"
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['calculate', ])
def calculate_task(message: telebot.types.Message):
    return


data_convert = '06.01.2023'

xml = etree.fromstring(
    requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={data_convert}").text.encode("1251"))


JPY_V = float(xml.find('Valute[@ID="R01820"]/Value').text.strip("\"").replace(",", "."))
JPY_R = int(xml.find('Valute[@ID="R01820"]/Nominal').text.strip("\"").replace(",", "."))
BYN_V = float(xml.find('Valute[@ID="R01090B"]/Value').text.strip("\"").replace(",", "."))
BYN_R = int(xml.find('Valute[@ID="R01090B"]/Nominal').text.strip("\"").replace(",", "."))
USD_V = float(xml.find('Valute[@ID="R01235"]/Value').text.strip("\"").replace(",", "."))
USD_R = int(xml.find('Valute[@ID="R01235"]/Nominal').text.strip("\"").replace(",", "."))
EUR_V = float(xml.find('Valute[@ID="R01239"]/Value').text.strip("\"").replace(",", "."))
EUR_R = int(xml.find('Valute[@ID="R01239"]/Nominal').text.strip("\"").replace(",", "."))
CNY_V = float(xml.find('Valute[@ID="R01375"]/Value').text.strip("\"").replace(",", "."))
CNY_R = int(xml.find('Valute[@ID="R01375"]/Nominal').text.strip("\"").replace(",", "."))

logger.info(f'на {data_convert} : USD {USD_V / USD_R}')
logger.info(f'на {data_convert} : EUR {EUR_V / EUR_R}')
logger.info(f'на {data_convert} : CNY {CNY_V / CNY_R}')
logger.info(f'на {data_convert} : BYN {BYN_V / BYN_R}')
logger.info(f'на {data_convert} : JPY {JPY_V / JPY_R}')

# Запуск полинга
bot.polling(none_stop=True)