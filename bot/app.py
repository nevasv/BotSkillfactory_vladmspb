# bot из задания 5.6 . Итоговый проект
# -*- coding: utf-8 -*-
import datetime
import time
import os
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
class ModuleException(Exception):
    """ Ошибки здесь - общий класс"""


class MyException(ModuleException):
    """ Мои исключения"""

    def __init__(self, *args):
        super().__init__(*args)
        self.msg = args if args else None
        # if args:
        #     self.msg = args
        # else:
        #     self.msg = None

    def __str__(self):
        return f"Ошибка: {self.msg}"


bot = telebot.TeleBot(TOKEN)

val_list = {
    '1': 'руб',
    '2': 'usd',
    '3': 'eur',
    '4': 'cny',
    '5': 'byn',
    '6': 'jpy'

}


class CurrencyCalculate:
    """ Преобразование даннвх и расчеты"""

    def __init__(self, data1, data2, value_input: float, action='convert', *args):
        self.data1 = data1
        self.data2 = data2
        self.value_input = value_input
        self.action = action
        self.data1_v = None
        self.data2_v = 1
        self.data1_r = None
        self.data2_r = None
        self.data_convert = f"{datetime.datetime.now():%d.%m.%Y}"
        self.str_inf = None

    def input_task(self, action, ):
        pass

    def get_result(self):
        pass

    def get_info_quote(self, X):
        """ Получение котировки валюты в рублях с сайта по введённому её номеру в списке"""
        ID = {'2': "R01235",
              '3': 'R01239',
              '4': 'R01375',
              '5': 'R01090B',
              '6': 'R01820'}
        keys = ID[X]
        connection_timeout = 30  # seconds
        start_time = time.time()
        while True:
            try:
                self.str_inf = etree.fromstring(
                    requests.get(
                        f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={self.data_convert}").text.encode(
                        "1251"))
                break
            except requests.ConnectionError:
                if time.time() > start_time + connection_timeout:
                    raise Exception(
                        'Unable to get updates after {} seconds of ConnectionErrors'.format(connection_timeout))
                else:
                    time.sleep(1)  # attempting once every second

        data_v = float(self.str_inf.find(f"Valute[@ID='{keys}']/Value").text.strip("\"").replace(",", "."))
        data_r = float(self.str_inf.find(f"Valute[@ID='{keys}']/Nominal").text.strip("\"").replace(",", "."))

        return data_v / data_r


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
           f' 1. Рубль              \n' \
           f' 2. Доллар США              : {USD_V / USD_R}\n' \
           f' 3. Евро                             : {EUR_V / EUR_R}\n' \
           f' 4. Китайский юань       : {CNY_V / CNY_R}\n' \
           f' 5. Беларусский рубль : {BYN_V / BYN_R}\n' \
           f" 6. Японская йена         : {i_01.get_info_quote('6')}"
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert_currency(message: telebot.types.Message):
    user_input = message.text.split(' ')
    if len(user_input) != 3:
        logger.warning('Значений нужно ввести  три')
        raise MyException('Значений нужно ввести  три')

    float_lst = [float(item) for item in user_input]
    print(float_lst)

    code1, code2, value_cur = user_input

    text = f"Конвертировать {value_cur} {val_list[code1]} в {val_list[code2]} !! произвести расчет? /calc"
    bot.send_message(message.chat.id, text)
    return float_lst


data_convert = f"{datetime.datetime.now():%d.%m.%Y}"

i_01 = CurrencyCalculate(2, 4, 200)
test = i_01.get_info_quote('6')
print(test)

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
