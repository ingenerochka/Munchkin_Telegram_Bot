"""
Модуль содержит неизменяемые данные словарей и конфигураций для работы бота
"""
import os

import logging

# Данные бота
token = os.environ.get('Munchkin_Telegram_Bot_Token')

# список ID администраторов
#admins_list = [1803096758]

# уровень логирования
log_level = logging.INFO

# количество ключей за заявку каждого типа
task_types = {
    "Upgrade (Обн. версии ПО или апп. конфигурации)": 9,
    "Профвизит": 6,
    "Администрирование по запросу": 4,
    "Консультации клиентов": 6,
    "Другие работы": 2,
    "Мониторинг системы": 2,
    "Устранение инцидента (Другое)": 10,
    "Устранение инцидента по условиям сервисного контракта": 10,
    "Консультация клиентов": 6,
    "Ошибки в работе": 10,
    'Регламентные работы': 2,
    'Ордер': 2,
    'Внедрение': 2
}

# данные для подключения к БД
DB_CONFIG = {
    "host": "127.0.0.1",
    "database_main": "munchkin_bot_main",
    "database_inventory": "munchkin_bot_user_inventory",
    "user": "postgres",
    "password": "Vfhbz",
    "port": "5432"
}

# путь к файлу excel
excel_path = r"excel\tasks_table.xlsx"

# путь к файлу с логами
log_path = r"logs\munchkin_bot.log"
log_dir = 'logs'
log_filename = 'munchkin_bot.log'

# путь к файлу с ошибками
error_path = r'errors\errors.doc'

# Количество ключей, необходимых для открытия двери
keys_for_open_door = 3

# Соответствие очков и уровней пользователя
levels_table = {
    1: range(0, 100),
    2: range(100, 200),
    3: range(200, 400),
    4: range(400, 700),
    5: range(700, 1000),
    6: range(1000, 1500),
    7: range(1500, 2000),
    8: range(2000, 3000),
    9: range(3000, 4000),
    10: range(4000, 5000)
}