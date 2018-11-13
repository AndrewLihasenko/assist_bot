# -*- coding: utf-8 -*-
import datetime
import subprocess

import schedule
import time
import re

import config
import telebot
from telebot import types
import MySQLdb
from telegram_bot_users import *

# Константы для указания шагов при вводе пароля пользователем
TEAM_USER_LOGGING = 0
TEAM_USER_ACCEPTED = 1

# Структура данных для для списка пользователей бота
team_users = TeamUserList()

bot = telebot.TeleBot(config.token)  # токен бота, хранится в config

admin_chat_id = 000111222  # нужен реальный chat_id

user_step = {}
user_active_dialog = {}
reply_data_db = {}

current_shown_dates = {}

full_data = ''
str_date = []


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать. Я ваш персональный помощник")


@bot.message_handler(commands=['help'])
def help(message):
        bot.send_message(message.chat.id, '/start - приветствие'
                          '\n/help - получение справки по командам'
                          '\n/menu - всплывающее меню с кнопками'
                          '\n/osmotry - получение даты осмотра и количества осмотренного оборудования'
                          '\n/defecty - получение информации об оборудовании отработавшем с дефектами'
                          '\n/prostoi - получение информации о простоях оборудования'
                          '\n/pdf - скачать отчеты в формате PDF'
                          '\n/on - стать зарегистрированным пользователем и получать ежедневную рассылку'
                          '\n/off - исключение из зарегистрированных пользователей'
                          '\n id - получить id пользователя ')


# получение id пользователя при вводе 'id'
@bot.message_handler(func=lambda message: message.text == "id" or
                                          message.text == "ID" or
                                          message.text == "Id")
def get_id(message):
    user = {}
    name = message.chat.first_name
    user[str(name)] = message.chat.id
    for name in user:
        bot.send_message(message.chat.id, '%s: %s' % (name, user[name]))


# Отправка отчета 'otchet_L1.pdf'. Только пользователям с id хранящемся в users_chat_id
def report_L1():
    users_chat_id = [111222333, 222333444, 444555666]
    try:
        for chat_id in users_chat_id:
            pdf = open('c:/QRTOOLS/L1/otchet_L1.pdf', 'rb')
            bot.send_document(chat_id, pdf)
    except FileNotFoundError as e:
        for chat_id in users_chat_id:
            bot.send_message(chat_id, 'Данный файл отсутствует')
        print(e)


# Отправка отчета 'otchet_L2.pdf'. Только пользователям с id хранящемся в users_chat_id
def report_L2():
    users_chat_id = [111222333, 222333444, 444555666]
    try:
        for chat_id in users_chat_id:
            pdf = open('c:/QRTOOLS/L2/otchet_L2.pdf', 'rb')
            bot.send_document(chat_id, pdf)
    except FileNotFoundError as e:
        for chat_id in users_chat_id:
            bot.send_message(chat_id, 'Данный файл отсутствует')
        print(e)


# Отправка отчета 'otchet_L3.pdf'. Только пользователям с id хранящемся в users_chat_id
def report_L3():
    users_chat_id = [111222333, 222333444, 444555666]
    try:
        for chat_id in users_chat_id:
            pdf = open('c:/QRTOOLS/L3/otchet_L3.pdf', 'rb')
            bot.send_document(chat_id, pdf)
    except FileNotFoundError as e:
        for chat_id in users_chat_id:
            bot.send_message(chat_id, 'Данный файл отсутствует')
        print(e)


# Отправка отчета 'otchet_color.pdf'. Только пользователям с id хранящемся в users_chat_id.
def report_color():
    users_chat_id = [111222333, 222333444, 444555666]
    try:
        for chat_id in users_chat_id:
            pdf = open('c:/QRTOOLS/COLOR/otchet_color.pdf', 'rb')
            if pdf: 
                bot.send_document(chat_id, pdf)
            else:
                subprocess.call('c:/USR/otchet/otchet_color.bat', shell=True)  # запуск файла
                time.sleep(5)  # таймаут
                pdf = open('c:/QRTOOLS/COLOR/otchet_color.pdf', 'rb')
                bot.send_document(chat_id, pdf)
    except FileNotFoundError as e:
        for chat_id in users_chat_id:
            bot.send_message(chat_id, 'Данный файл отсутствует')
        print(e)


# Получение данных по осмотрам, дефектам и простоям за сегодня. Отправляется ежедневно всем зарегистрированным пользователям в 19.00
def data_for_today():
    date = datetime.date.today()
    conn1 = MySQLdb.connect(host='localhost', user='root', passwd='passwd', db='vt', charset="utf8")
    cursor1 = conn1.cursor()
    # Запрос в mysql
    sql1 = """ select date_format()
        left JOIN ..."""
    cursor1.execute(sql1)
    data1 = cursor1.fetchall()
    for rows in data1:
        local_date, osmotr, smena = rows
        f_data = ('%(date)s - проведен осмотр %(osmotr)s единиц из %(smena)s'
                  % {"date": local_date, "osmotr": osmotr, "smena": smena})
        for user in team_users:
            bot.send_message(user.chat_id, f_data)
        if not f_data:
            for user in team_users:
                bot.send_message(user.chat_id, "Осмотры не проводились")
    conn1.close()
    conn2 = MySQLdb.connect(host='localhost', user='root', passwd='passwd', db='vt', charset="utf8")
    cursor2 = conn2.cursor()
    sql2 = """select ...
      left JOIN..."""
    cursor2.execute(sql2)
    data2 = cursor2.fetchall()
    for row in data2:
        if row is None: continue
        name2 = ''.join(row[4:])
        param2 = ''.join(row[:1])
        for user in team_users:
            bot.send_message(user.chat_id,
                             '%(date)s - %(name)s, %(param)s'
                             % {"date": date, "name": name2, "param": param2})
    conn2.close()
    conn3 = MySQLdb.connect(host='localhost', user='root', passwd='passwd', db='vt', charset="utf8")
    cursor3 = conn3.cursor()
    sql3 = """ select...
      left JOIN..."""
    cursor3.execute(sql3)
    data3 = cursor3.fetchall()
    for row in data3:
        if row is None: continue
        param3 = ', '.join([i for i in row[1:16] if not (i in ['', 'None', None])])
        name3 = ''.join(row[16:])
        for user in team_users:
            bot.send_message(user.chat_id,
                             '%(date)s - %(name)s. \nСледующие параметры отработали с отклонениями: \n%(params)s'
                             % {"date": date, "name": name3, "params": param3})
    conn3.close()
    if not team_users:
        bot.send_message(admin_chat_id, 'Нет зарегистрированных пользователей')


# кнопка 'Осмотры'
@bot.message_handler(commands=['osmotry'])
def inspections(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, "Введите пожалуйста дату вида: \n2018-05-16", reply_markup=markup)
    bot.register_next_step_handler(message, get_day_insp)


# обработчик кнопки 'Осмотры'
def get_day_insp(message):
    mesg = message.text
    if mesg.capitalize().startswith("2"):
        raw_date = re.findall('[\d]+', mesg)  # регулярное выражение
        if len(raw_date) < 3:
            bot.send_message(message.chat.id, 'Вы ввели не полную дату! Введите еще раз')
            bot.register_next_step_handler(message, get_day_insp)
            return
        year, month, day = raw_date
        if 2018 < int(year) or int(month) > 12:
            bot.send_message(message.chat.id, 'Вы ввели неверную дату! Введите еще раз')
            bot.register_next_step_handler(message, get_day_insp)
            return
        date = '-'.join([year, month, day])

        # подключение к базе данных
        conn = MySQLdb.connect(host='localhost', user='root', passwd='passwd', db='vt')
        cursor = conn.cursor()
        sql = ("""select...
                left JOIN... """ % (date, date))

        cursor.execute(sql)
        data = cursor.fetchall()
        for rows in data:
            local_date, osmotr, smena = rows
            f_data = ('%(date)s - проведен осмотр %(osmotr)s единиц из %(smena)s'
                      % {"date": local_date, "osmotr": osmotr, "smena": smena})
            bot.send_message(message.chat.id, f_data)
            conn.close()


# кнопка 'Дефекты'
@bot.message_handler(commands=['defecty'])
def defects(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "Введите пожалуйста дату вида: \n2018-05-16", reply_markup=markup)
    bot.register_next_step_handler(message, get_day_def)


# обработчик кнопки 'Дефекты'
def get_day_def(message):
    mesg = message.text
    if mesg.capitalize().startswith("2"):
        raw_date = re.findall('[\d]+', mesg)
        if len(raw_date) < 3:
            bot.send_message(message.chat.id, 'Вы ввели неполную дату! Введите еще раз')
            bot.register_next_step_handler(message, get_day_def)
            return
        year, month, day = raw_date
        if 2018 < int(year) or int(month) > 12:
            bot.send_message(message.chat.id, 'Вы ввели неверную дату! Введите еще раз')
            bot.register_next_step_handler(message, get_day_def)
            return
        date = '-'.join([year, month, day])

        # подключение к базе данных
        conn = MySQLdb.connect(host='localhost', user='root', passwd='password', db='vt', charset="utf8")
        cursor = conn.cursor()
        sql = ("""select ...
                left JOIN...""" % (date))

        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            if row is None: continue
            params = ', '.join([i for i in row[1:16] if not (i in ['', 'None', None])])
            name = ''.join(row[16:])
            bot.send_message(message.chat.id,
                             '%(date)s - %(name)s. \nСледующие параметры отработали с отклонениями: \n%(params)s'
                             % {"date": date, "name": name, "params": params})
        conn.close()


# кнопка 'Простои'
@bot.message_handler(commands=['prostoi'])
def downtime(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, "Введите пожалуйста дату вида: \n2018-05-16", reply_markup=markup)
    bot.register_next_step_handler(message, get_day_down)


# обработчик кнопки 'Простои'
def get_day_down(message):
    mesg = message.text
    if mesg.capitalize().startswith("2"):
        raw_date = re.findall('[\d]+', mesg)
        if len(raw_date) < 3:
            bot.send_message(message.chat.id, 'Вы ввели не полную дату! Введите еще раз')
            bot.register_next_step_handler(message, get_day_down)
            return
        year, month, day = raw_date
        if 2018 < int(year) or int(month) > 12:
            bot.send_message(message.chat.id, 'Вы ввели неверную дату! Введите еще раз')
            bot.register_next_step_handler(message, get_day_down)
            return
        date = '-'.join([year, month, day])

        # подключение к базе данных
        conn = MySQLdb.connect(host='localhost', user='root', passwd='passwd', db='vt', charset="utf8")
        cursor = conn.cursor()
        sql = (""" select...
                left JOIN...""" % (date))

        cursor.execute(sql)
        data = cursor.fetchall()
        global full_data
        for row in data:
            if row is None: continue
            name = ''.join(row[4:])
            param = ''.join(row[:1])
            bot.send_message(message.chat.id,
                             '%(date)s - %(name)s, %(param)s'
                             % {"date": date, "name": name, "param": param})
        conn.close()

# Кнопка 'Скачать в PDF'. Формирование  inline кнопок для скачивания 4 типов отчетов 
@bot.message_handler(commands=['pdf'])
def download_pdf(message):
    keyboard = types.InlineKeyboardMarkup()
    btn_report_L1 = types.InlineKeyboardButton(text="Отчет о простоях критичного оборудования", callback_data="L1")
    btn_report_L2 = types.InlineKeyboardButton(text="Отчет о простоях и дефектах более 3 дней", callback_data="L2")
    btn_report_L3 = types.InlineKeyboardButton(text="Ежедневный отчет о простоях и дефектах", callback_data="L3")
    btn_report_L4 = types.InlineKeyboardButton(text="График - отчет об осмотре оборудования", callback_data="color")
    keyboard.add(btn_report_L1)
    keyboard.add(btn_report_L2)
    keyboard.add(btn_report_L3)
    keyboard.add(btn_report_L4)
    bot.send_message(message.chat.id, "Выберите тип отчета:", reply_markup=keyboard)


# Обработчики 4-х inline кнопок
@bot.callback_query_handler(func=lambda call: call.data)
def callback_inline(call):
    if call.message:
        if call.data == "L1":
            chat_id = call.message.chat.id
            try:
                pdf = open('c:/QRTOOLS/L1/otchet_L1.pdf', 'rb')
                bot.send_document(chat_id, pdf)
                bot.answer_callback_query(call.id, text="Файл выбран")
            except FileNotFoundError as e:
                # если файла 'otchet_L1.pdf' нет, запуск 'otchet_L1.bat' для формирования pdf.
                bot.send_message(chat_id, "Внимание - файл формируется! Подождите около 5 сек. и повторите попытку")
                subprocess.call('c:/USR/otchet/otchet_L1.bat', shell=True)  # запуск файла на исполнение
                print(e) # отчет об ошибке в консоль
                # обязательный ответ на запрос от inline keyboard
                bot.answer_callback_query(call.id, text="Файл выбран")
        elif call.data == "L2":
            chat_id = call.message.chat.id
            try:
                pdf = open('c:/QRTOOLS/L2/otchet_L2.pdf', 'rb')
                bot.send_document(chat_id, pdf)
                bot.answer_callback_query(call.id, text="Файл выбран")
            except FileNotFoundError as e:
                # если файла 'otchet_L2.pdf' нет, запуск 'otchet_L2.bat' для формирования pdf.
                bot.send_message(chat_id, "Внимание - файл формируется! Подождите около 5 сек. и повторите попытку")
                subprocess.call('c:/USR/otchet/otchet_L2.bat', shell=True)
                print(e)
                bot.answer_callback_query(call.id, text="Файл выбран")
        elif call.data == "L3":
            chat_id = call.message.chat.id
            try:
                pdf = open('c:/QRTOOLS/L3/otchet_L3.pdf', 'rb')
                bot.send_document(chat_id, pdf)
                bot.answer_callback_query(call.id, text="Файл выбран")
            except FileNotFoundError as e:
                # если файла 'otchet_L3.pdf' нет, запуск 'otchet_L3.bat' для формирования pdf.
                bot.send_message(chat_id, "Внимание - файл формируется! Подождите около 5 сек. и повторите попытку")
                subprocess.call('c:/USR/otchet/otchet_L3.bat', shell=True)
                print(e)
                bot.answer_callback_query(call.id, text="Файл выбран")
        elif call.data == "color":
            chat_id = call.message.chat.id
            try:
                pdf = open('c:/QRTOOLS/COLOR/otchet_color.pdf', 'rb')
                bot.send_document(chat_id, pdf)
                bot.answer_callback_query(call.id, text="Файл выбран")
            except FileNotFoundError as e:
                # если файла 'otchet_color.pdf' нет, запуск 'otchet_color.bat' для формирования pdf.
                bot.send_message(chat_id, "Внимание - файл формируется! Подождите около 5 сек. и повторите попытку")
                subprocess.call('c:/USR/otchet/otchet_color.bat', shell=True)
                print(e)
                bot.answer_callback_query(call.id, text="Файл выбран")


# подключение пользователей к зарегистрированным
@bot.message_handler(commands=['on'])
def subscribe_chat(message): 
    if message.chat.id in team_users:
        bot.reply_to(message, "Вы зарегистрированный пользователь")
    else:
        user_step[message.chat.id] = TEAM_USER_LOGGING
        bot.reply_to(message, "Введите пароль")


# запрос пароля
@bot.message_handler(func=lambda message: user_step.get(message.chat.id) == TEAM_USER_LOGGING)
def team_user_login(message):  
    if message.text == 'password_one':  # пароль
        team_users.add(TeamUser(message.chat.id))
        bot.send_message(admin_chat_id, '%s: %s - подключился к зарегистрированным пользователям'
                         % (message.chat.id, message.chat.first_name))
        user_step[message.chat.id] = TEAM_USER_ACCEPTED
        bot.reply_to(message, "Теперь вы зарегистрированный пользователь и будете получать уведомления")
    else:
        bot.reply_to(message, "Неправильный пароль, попробуйте еще")
        if message.text == '/off':
            team_user_logout(message)
            user_step[message.chat.id] = TEAM_USER_ACCEPTED


# исключение пользователей из зарегистрированных
@bot.message_handler(commands=['off'])
def team_user_logout(message): 
    if message.chat.id not in team_users:
        bot.reply_to(message, "Вы не зарегистрированный пользователь")
    else:
        team_users.remove_by_chat_id(message.chat.id)
        bot.reply_to(message, "Теперь вы не зарегистрированный пользователь и не будете получать уведомления")


# запуск меню с кнопками
@bot.message_handler(commands=['menu'])
def keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Осмотры')
    itembtn2 = types.KeyboardButton('Дефекты')
    itembtn3 = types.KeyboardButton('Простои')
    itembtn4 = types.KeyboardButton('Скачать в PDF')
    markup.row(itembtn1, itembtn2, itembtn3)
    markup.row(itembtn4)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


# запуск обработчиков кнопок
@bot.message_handler(content_types=['text'])
def btnmessage(message):
    if message.text == 'Осмотры':
        inspections(message)
    elif message.text == 'Дефекты':
        defects(message)
    elif message.text == 'Простои':
        downtime(message)
    elif message.text == 'Скачать в PDF':
        download_pdf(message)


''' Отправка файлов по расписанию. Используется библиотека schedule. 
Если нужна отправка определенным пользователям, нужно id добавить к users_chat_id соответствующей функции, кроме data_for_today. 
В data_for_today пользователи добавляются автоматически по запросу /on.
Если нужна отправка по определенным дням то: schedule.every().wednesday.at("08:00").do(название_функции)'''
schedule.every().day.at("08:08").do(report_color)
schedule.every().day.at("07:53").do(report_L3)
schedule.every().day.at("07:58").do(report_L2)
schedule.every().day.at("08:03").do(report_L1)
schedule.every().day.at("19:00").do(data_for_today)


# запуск бота
bot.polling(none_stop=True)
