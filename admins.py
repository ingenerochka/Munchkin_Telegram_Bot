"""
Модуль содержит функции для проверки прав и взаимодействия с администраторами
"""

import logging

import psycopg
import telebot

import databases
import configs


def admin_check(user_id: int) -> bool:
    """
    Функция проверяет, имеет ли пользователь права администратора
    :param user_id: Уникальный ID пользователя в Телеграм
    :return: True, если пользователь имеет права администратора, False если нет
    """
    conn, cursor = databases.connet_to_db(configs.DB_CONFIG['database_main'])
    try:
        cursor.execute(
            query='SELECT is_admin FROM user_data WHERE user_id=%s',
            params=(user_id,)
        )
        result = cursor.fetchone()[0]
        logging.info(f'Права пользователя проверены. Пользователь {user_id} админ {bool(result)}')
        return bool(result)
    except psycopg.Error as error:
        logging.error(f'Ошибка при проверке прав администратора пользователя {user_id}'
                      f'{error}')
        return False
    finally:
        conn.close()


def get_admins() -> list[int] | None:
    """
    Функция проходит по всей БД пользователей и проверяет, есть ли у пользователя права администратора
    :return: список ID пользователей с правами администратора либо ничего в случае ошибки
    """
    conn, cursor = databases.connet_to_db(configs.DB_CONFIG['database_main'])
    try:
        cursor.execute(
            query='SELECT user_id FROM user_data WHERE is_admin=True'
        )
        admins_list = cursor.fetchall()
        logging.info(f'Сформирован список администраторов: {admins_list}')
        return admins_list
    except psycopg.Error as error:
        logging.error(f'Ошибка при формировании списка администраторов'
                      f'{error}')
        return None
    finally:
        conn.close()


def admin_new_user_alarm(new_user_name: str, new_user_id: int, bot: telebot.TeleBot):
    """
    Функция рассылает администраторам сообщение, когда в боте регистрируется новый пользователь
    :param new_user_name: Имя нового зарегистрированного пользователя
    :param new_user_id: Id нового зарегистрированного пользователя
    :param bot: Объект сессии Телеграм
    :return: Nome
    """
    admins_list = get_admins()
    print(admins_list)
    for admin_id in admins_list:
        bot.send_message(
            chat_id=admin_id[0],
            text=f'В боте Инженерский Манчкин зарегистрировался новый пользователь\n'
                 f'Имя пользователя: <b>{new_user_name}</b>\n'
                 f'ID пользователя: <b>{new_user_id}</b>',
            parse_mode='HTML'
        )
        logging.info(f'Администратор {admin_id[0]} уведомлен о новом пользователе')
