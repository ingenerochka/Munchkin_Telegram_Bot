"""
Модуль для вспомогательных функций
"""

from telebot import types
from typing import Dict, Any

import databases
import configs


def converter_user_data(message: types.Message) -> Dict[str, Any]:
    """
    Функция конвертирует часть данных о пользователе из формата bjson в словарь
    :param message: Объект, содержащий информацию о сообщении пользователя
    :return: Словарь, содержащий данные о пользователе, написавшем сообщение
    """
    user = message.from_user

    user_data = {
        'id': user.id,
        'first_name': user.last_name,
        'last_name': user.last_name,
        'full_name': user.full_name,
        'username': user.username,
        'language_code': user.language_code,
        'is_bot': user.is_bot,
        'is_premium': user.is_premium
    }
    return user_data


def get_user_info(user_id: int) -> Dict[str, Any]:
    """
    Функция конвертирует кортеж с данными пользователя, полученными из БД, в словарь
    :param user_id: Уникальный ID пользователя в Телеграм
    :return: Словарь, содержащий данное о пользователе бота
    """
    data = databases.get_user_profile(user_id)
    user_data = {
        'hero_name': data[0],
        'level': data[1],
        'points': data[2],
        'coins': data[3],
        'keys': data[4],
        'race': data[5],
        'hero_class': data[6],
        'title': data[7]
    }
    return user_data


def get_monster_info(monster: tuple) -> Dict[str, Any]:
    """
    Функция конвертирует кортеж с данными о монстре, полученными из БД, в словарь
    :param monster: Кортеж с информацией о монстре
    :return: Словарь, содержащий данные о монстре
    """
    monster_data = {
        'monster_id': monster[0],
        'monster_name': monster[1],
        'description': monster[2],
        'strength': monster[3],
        'trophy': monster[4],
        'scores': monster[5],
        'escalation': monster[6],
        'escalation_id': monster[7],
    }
    return monster_data


def get_thing_info(thing: tuple) -> Dict[str, Any]:
    """
    Функция конвертирует кортеж с данными о вещи в инвентаре пользователя, полученными из БД, в словарь
    :param thing: Кортеж с информацией о вещи в инвентаре пользователя
    :return: Словарь, содержащий данные о вещи в инвентаре пользователя
    """
    thing_data = {
        'thing_id': thing[0],
        'thing_name': thing[1],
        'type': thing[2],
        'description': thing[3],
        'conditions': thing[4],
        'price': thing[5],
        'state_active': thing[6],
        'bonus': thing[7],
    }
    return thing_data


def keys_checking(user_id: int):
    """
    Функция проверяет, достаточно ли у пользователя для открытия двери
    :param user_id: Уникальный ID пользователя в Телеграм
    :return: True или False в зависимости от кол-ва ключей, количество дверей, которые можно открыть
    """
    keys = get_user_info(user_id)['keys']
    doors = keys / configs.keys_for_open_door
    if doors >= 1:
        return True, doors
    else:
        return False, doors