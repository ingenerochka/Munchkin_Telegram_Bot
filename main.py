"""
Основной модуль с кодом Телеграм-бота.
Обрабатывает сообщения от пользователя, посылает сообщения пользователю, совершает запросы к остальным модулям.
"""

import logging

import requests.exceptions
import telebot
from telebot.types import Message

import callbacks
import databases
import configs
import logs
import errors
import reports
import supports
import admins
import keyboards

# настройка логирования
logs.setup_logging()

bot = telebot.TeleBot(configs.token)


@bot.message_handler(commands=['start'])
def start_text(message: Message) -> None:
    """
    Функция обработки сообщений на команду start, приветствует пользователя
    :param message: Объект, содержащий информацию о сообщении пользователя
    :return: None
    """
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_data = supports.converter_user_data(message=message)
    logging.info(f'Пользователь {message.from_user.full_name} запустил бота')
    databases.insert_user_data_in_bd(user_id=user_id, user_data=user_data, user_name=user_name)
    databases.create_user_inventory_table(user_id)
    bot.send_message(message.chat.id, f'Здравствуй, {user_name}!\n'
                                      'Добро пожаловать в Инженерский Манчкин!\n'
                                      'Для просмотра Главного меню нажми команду /menu')
    admins.admin_new_user_alarm(user_name, user_id, bot)
    return


@bot.message_handler(commands=['menu'])
def menu_text(message) -> None:
    """
    Функция обработки сообщений на команду menu, вызывает клавиатуру Главного меню
    :param message: Объект, содержащий информацию о сообщении пользователя
    :return: None
    """
    bot.send_message(chat_id=message.chat.id,
                     text='Главное меню',
                     reply_markup=keyboards.menu_keyboard()
                     )
    logging.info('Пользователь запросил Главное меню')
    return


@bot.callback_query_handler(func=lambda message: True)
def logic_inline(call) -> None:
    """
    Функция обрабатывает коллбеки от Инлайн-клавиатуры, вызываемой командой menu
    :param call: Строка с коллбеком
    :return: None
    """
    user_id = call.from_user.id
    callbacks.get_callback(bot, call, user_id)


@bot.message_handler(content_types=['document'])
def handler_docs(message) -> None:
    """
    Функция обработки загружаемой в бота Excel-таблицы. Получает таблицу с серверов Телеграмма,
    распарсивает и записывает данные в БД.
    :param message: Объект, содержащий информацию о сообщении пользователя
    :return: None
    """
    file_name = message.document.file_name
    file_info = bot.get_file(file_id=message.document.file_id)
    downloader_file = bot.download_file(file_path=file_info.file_path)

    with open(r'downloads\\' + str(file_name), 'wb') as new_file:
        new_file.write(downloader_file)

    bot.send_message(message.chat.id, text='Отчет по выполненным заявкам загружен')
    logging.info(f'Загружен и скачан файл {file_name}')

    table = reports.parse_excel(fr'downloads\{file_name}')
    table.pop(0)
    for engineer, task in table:
        keys = reports.convert_to_keys(task)
        if keys > 0:
            reports.update_keys(engineer, keys)
    bot.send_message(message.chat.id, text='Завершена обработка загруженного файла. '
                                           'Выполненные заявки переведены в ключи')
    return


def run_bot() -> None:
    """
    Функция запускает работу бота в бесконечном цикле
    :return: None
    """
    logging.info(f'Бот запущен')
    while True:
        try:
            bot.polling()
            # Опрос серверов Телеграм, есть ли сообщения для бота
        except requests.exceptions.ConnectionError as error:
            logging.error(f'Обрыв соединения. Ошибка: {error}')
            errors.error_save(short_error=error, bot=bot)
        except BaseException as base_error:
            logging.error(f'Ошибка: {base_error}')
            errors.error_save(short_error=base_error, bot=bot)
        logging.warning('Бот перезапущен')


if __name__ == "__main__":
    run_bot()

# TODO: вспомнить, как включать через батник