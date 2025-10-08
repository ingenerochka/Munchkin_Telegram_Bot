"""
Модуль для обработки ошибок
"""

import logging
import traceback

import telebot

import admins
import configs


def error_save(short_error: Exception, bot: telebot.TeleBot) -> None:
    """
    Функция записывает полный текст ошибки в файл и оправляет администраторам сообщение по их id в Телеграм,
    в котором указана краткая информация об ошибке и файл с ошибкой.
    :param short_error: Краткая информация об ошибке
    :param bot: Объект, содержащий информацию о боте
    :return: None
    """
    long_error = traceback.format_exc()

    with open(configs.error_path, 'w') as file:
        file.write(long_error)
    admins_list = admins.get_admins()
    for id_admin in admins_list:
        try:
            with open(configs.error_path, 'rb') as file:
                bot.send_document(
                    chat_id=id_admin,
                    document=file,
                    caption='Произошла ошибка в работе бота!\n'
                            '\n'
                            f'Краткая ошибка: <b>{short_error}</b>',
                    parse_mode='HTML'
                )
            logging.info(f'Администратор {id_admin} успешно уведомлен об ошибке')
        except(Exception, BaseException):
            logging.error(f'Произошла ошибка при уведомлении администратора id {id_admin}')
