"""
Модуль для работы с базами данных
"""

import psycopg
import logging

from typing import Dict, Any, Tuple
from psycopg.types.json import Jsonb

import configs


def connet_to_db(dbname: str) -> Tuple[psycopg.Connection | None, psycopg.Cursor | None]:
    """
    Функция устанавливает сессию с БД и создает курсор для взаимодействия с БД
    :return:переменные соединения с БД и курсор, либо ничего в случае ошибки подключения к БД
    """
    try:
        conn = psycopg.connect(
            f"dbname={dbname} "
            f"user={configs.DB_CONFIG['user']} "
            f"password={configs.DB_CONFIG['password']} "
            f"host={configs.DB_CONFIG['host']} "
            f"port={configs.DB_CONFIG['port']} "
        )
        cursor = conn.cursor()
        logging.info(f"Успешное подключение к БД {dbname}")
        return conn, cursor

    except (Exception, psycopg.Error) as error:
        logging.exception(f"Ошибка при подключении к БД {dbname}: {error}")
        return None, None


def insert_user_data_in_bd(user_id: int, user_data: Dict[str, Any], user_name: str) -> None:
    """
    Функция добавляет или обновляет информацию о пользователе в таблицу в БД пользователей
    :param user_id: уникальный номер пользователя в Телеграм
    :param user_data: данные об учетной записи пользователя в Телеграм
    :param user_name: имя пользователя в Телеграм
    :return: None
    """
    conn, cursor = connet_to_db(configs.DB_CONFIG['database_main'])
    try:
        query = ('INSERT INTO user_data '
                 '(user_id, telegram_data, verification, is_admin, level, points, keys, coins, '
                 'name, race, class, title, inventory_id) '
                 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
                 'ON CONFLICT (user_id) '
                 'DO UPDATE SET (user_id, telegram_data, inventory_id) = '
                 '(EXCLUDED.user_id, EXCLUDED.telegram_data, EXCLUDED.inventory_id);')
        cursor.execute(query=query,
                       params=(user_id, Jsonb(user_data), False, False,
                               0, 0, 0, 0, user_name, "Человек", "Нет", "Нет", f'inventory_{user_id}')
                       )
        conn.commit()
        logging.info('Данные пользователя успешно сохранены в user_data')
    except psycopg.Error as error:
        logging.error(f'Ошибка записи в таблицу user_data: {error}')
    finally:
        conn.close()


def create_user_inventory_table(user_id: int) -> None:
    """
    Функция создает таблицу инвентаря для нового пользователя
    :param user_id: уникальный номер пользователя в Телеграм
    :return: None
    """
    conn, cursor = connet_to_db(configs.DB_CONFIG['database_inventory'])
    try:
        cursor.execute(query=f'CREATE TABLE IF NOT EXISTS inventory_{user_id} ('
                             'id INT PRIMARY KEY NOT NULL, '
                             'name TEXT, '
                             'type TEXT, '
                             'description TEXT, '
                             'bonus INT, '
                             'conditions TEXT, '
                             'price INT, '
                             'state_active BOOLEAN);')
        conn.commit()
        logging.info(f'Для пользователя ID {user_id} создана таблица Инвентаря')
    except psycopg.Error as error:
        logging.error(f'Ошибка при создании таблицы Инвентаря для пользователя {user_id} : {error}')
    finally:
        conn.close()


def get_user_profile(user_id: int) -> list[int]:
    """
    Функция выводит информацию о пользователе при нажатии кнопки Профиль в Главном меню
    :param user_id: Уникальный ID пользователя в Телеграм
    :return: список из значений строки пользователя из БД пользователей, содержащий данные о пользователе
    """
    conn, cursor = connet_to_db(configs.DB_CONFIG['database_main'])
    try:
        cursor.execute(
            query='SELECT name, level, points, coins, keys, race, class, title FROM user_data WHERE user_id=%s',
            params=(user_id,)
        )
        result = cursor.fetchone()
        logging.info(f'Передана информация о профиле пользователя ID {user_id}')
        return result
    except psycopg.Error as error:
        logging.error(f'Ошибка при выводе профиля пользователя ID {user_id} : {error}')
    finally:
        conn.close()


def get_user_inventory(user_id: int) -> list[int]:
    """
    Функция выводит информацию об инвентаре пользователя при нажатии кнопки Инвентарь в Главном меню
    :param user_id: Уникальный ID пользователя в Телеграм
    :return: список вещей с описанием, находящихся в инвентаре пользователя
    """
    conn, cursor = connet_to_db(configs.DB_CONFIG['database_inventory'])
    try:
        cursor.execute(
            query=f'SELECT id, name, type, description, conditions, price, state_active, bonus FROM inventory_{user_id}'
        )
        result = cursor.fetchall()
        logging.info(f'Передана информация о содержании инвентаря пользователя ID {user_id}')
        return result
    except psycopg.Error as error:
        logging.error(f'Ошибка при выводе инвентаря пользователя ID {user_id} : {error}')
    finally:
        conn.close()


def change_thing_status(user_id: int, thing_id: int, command: str) -> None:
    """
    Функция меняет статус вещи со снято на надето или с надето на снято в зависимости от команды
    :param user_id: Уникальный ID пользователя в Телеграм
    :param thing_id: Уникальный ID вещи пользователя в БД Инвентаря
    :param command: Строка с командой снять или надеть
    :return: None
    """
    conn, cursor = connet_to_db(configs.DB_CONFIG['database_inventory'])
    if command == 'puton':
        try:
            cursor.execute(
                query=f'SELECT type FROM inventory_{user_id} WHERE id=%s',
                params=(thing_id,)
            )
            thing_type = cursor.fetchone()[0]
            cursor.execute(
                query=f'UPDATE inventory_{user_id} SET state_active=False WHERE type=%s',
                params=(thing_type,)
            )
            cursor.execute(
                query=f'UPDATE inventory_{user_id} SET state_active=True WHERE id=%s',
                params=(thing_id,)
            )
            conn.commit()
            logging.info(f'Пользователь ID {user_id} надел вещь {thing_id}')
        except psycopg.Error as error:
            logging.error(f'Ошибка при попытке пользователя ID {user_id} надеть вещь {thing_id}: {error}')
        finally:
            conn.close()
    if command == 'putout':
        try:
            cursor.execute(
                query=f'UPDATE inventory_{user_id} SET state_active=False WHERE id=%s',
                params=(thing_id,)
            )
            conn.commit()
            logging.info(f'Пользователь ID {user_id} снял вещь {thing_id}')
        except psycopg.Error as error:
            logging.error(f'Ошибка при попытке пользователя ID {user_id} снять вещь {thing_id}: {error}')
        finally:
            conn.close()


def open_door(user_id: int, number_of_keys: int) -> None:
    """
    Функция вычитает потраченные ключи из БД пользователя при открытии двери
    :param user_id: Уникальный ID пользователя в Телеграм
    :param number_of_keys: Количество использованных ключей
    :return: None
    """
    conn, cursor = connet_to_db(configs.DB_CONFIG['database_main'])
    try:
        cursor.execute(
            query='UPDATE user_data SET keys=keys-%s WHERE user_id=%s',
            params=(number_of_keys, user_id)
        )
        conn.commit()
        logging.info(f'Пользователь ID {user_id} открыл дверь')
    except psycopg.Error as error:
        logging.error(f'Ошибка при попытке пользователя ID {user_id} открыть дверь: {error}')
    finally:
        conn.close()


def get_monster(user_level) -> list[int]:
    """
    Функция выбора случайного монстра для боя после открытия двери
    :param user_level: Уровень пользователя
    :return: Строку с данными о монстре
    """
    conn, cursor = connet_to_db(configs.DB_CONFIG['database_main'])
    try:
        cursor.execute(
            query='SELECT * FROM monster_data WHERE strength <= %s+25 ORDER BY RANDOM() LIMIT 1',
            params=(user_level,)
        )
        result = cursor.fetchone()
        logging.info(f'Выбран монстр для боя {result[1]}')
        return result
    except psycopg.Error as error:
        logging.error(f'Ошибка при выборе монстра для боя: {error}')
    finally:
        conn.close()


def get_trophy(db_name) -> list[int]:
    """
    Функция выбора случайного сокровища из БД Вещей, Монет или Рас и классов
    :param db_name: имя базы данных, откуда выбирать сокровище
    :return: Строку с данными о сокровище
    """
    conn, cursor = connet_to_db(configs.DB_CONFIG['database_main'])
    try:
        cursor.execute(
            query=f'SELECT * FROM {db_name} ORDER BY RANDOM() LIMIT 1')
        result = cursor.fetchone()
        logging.info(f'Выбрано сокровище {result[1]}')
        return result
    except psycopg.Error as error:
        logging.error(f'Ошибка при выборе сокровища: {error}')
    finally:
        conn.close()


def update_points(user_id: int, new_points: int) -> None:
    """
    Функция обновляет кол-во очков пользователя в БД пользователей
    :param user_id: Уникальный ID пользователя в Телеграм
    :param new_points: Новое значение очков пользователя
    :return:
    """
    conn, cursor = connet_to_db(configs.DB_CONFIG['database_main'])
    try:
        cursor.execute(
            query='UPDATE user_data SET points=%s WHERE user_id=%s',
            params=(new_points, user_id)
        )
        conn.commit()
        logging.info(f'Пользователь ID {user_id} получил очки')
    except psycopg.Error as error:
        logging.error(f'Ошибка при изменении кол-ва очков пользователя ID {user_id}: {error}')
    finally:
        conn.close()


def update_level(user_id: int, new_level: int) -> None:
    """
    Функция обновляет уровень пользователя в БД пользователей
    :param user_id: Уникальный ID пользователя в Телеграм
    :param new_level: Новое значение уровня пользователя
    :return:
    """
    conn, cursor = connet_to_db(configs.DB_CONFIG['database_main'])
    try:
        cursor.execute(
            query='UPDATE user_data SET level=%s WHERE user_id=%s',
            params=(new_level, user_id)
        )
        conn.commit()
        logging.info(f'Пользователь ID {user_id} получил новый уровень')
    except psycopg.Error as error:
        logging.error(f'Ошибка при изменении уровня пользователя ID {user_id}: {error}')
    finally:
        conn.close()


def update_coins(user_id: int, new_coins: int) -> None:
    """
    Функция обновляет количество монет пользователя в БД пользователей
    :param user_id: Уникальный ID пользователя в Телеграм
    :param new_coins: Новое значение количества монет пользователя
    :return:
    """
    conn, cursor = connet_to_db(configs.DB_CONFIG['database_main'])
    try:
        cursor.execute(
            query='UPDATE user_data SET coins=%s WHERE user_id=%s',
            params=(new_coins, user_id)
        )
        conn.commit()
        logging.info(f'Пользователь ID {user_id} получил монеты')
    except psycopg.Error as error:
        logging.error(f'Ошибка при получении монет пользователем ID {user_id}: {error}')
    finally:
        conn.close()


def update_race_class(user_id: int, type_race_class: str, new_race_class: int) -> None:
    """
    Функция добавляет новую расу или класс пользователя в БД пользователей
    :param user_id: Уникальный ID пользователя в Телеграм
    :param type_race_class: Тип, раса или класс
    :param new_race_class: Новая раса или класс
    :return:
    """
    conn, cursor = connet_to_db(configs.DB_CONFIG['database_main'])
    try:
        cursor.execute(
            query=f'UPDATE user_data SET {type_race_class}=%s WHERE user_id=%s',
            params=(new_race_class, user_id)
        )
        conn.commit()
        logging.info(f'Пользователь ID {user_id} получил расу/класс {new_race_class}')
    except psycopg.Error as error:
        logging.error(f'Ошибка при получении расы/класса {new_race_class} пользователем ID {user_id}: {error}')
    finally:
        conn.close()


def update_inventory(user_id: int, new_thing: list[int]) -> None:
    """
    Функция добавляет новую вещь в БД инвентаря пользователя
    :param user_id: Уникальный ID пользователя в Телеграм
    :param new_thing: Строка с данными о вещи
    :return:
    """
    thing_id = new_thing[0]
    name = new_thing[1]
    thing_type = new_thing[2]
    description = new_thing[3]
    conditions = new_thing[4]
    price = new_thing[5]
    bonus = new_thing[6]
    conn, cursor = connet_to_db(configs.DB_CONFIG['database_inventory'])
    try:
        cursor.execute(
            query=f'INSERT INTO inventory_{user_id} '
                  '(id, name, type, description, bonus, conditions, price, state_active) '
                  'VALUES (%s, %s, %s, %s, %s, %s, %s, %s);',
            params=(thing_id, name, thing_type, description, bonus, conditions, price, False)
        )
        conn.commit()
        logging.info(f'Пользователь ID {user_id} получил вещь {name}')
    except psycopg.Error as error:
        logging.error(f'Ошибка при получении вещи {name} пользователем ID {user_id}: {error}')
    finally:
        conn.close()