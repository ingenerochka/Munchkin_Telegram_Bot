"""
Модуль отвечает за получение пользователем бонусов при победе над монстром
"""
import random

import telebot
from telebot import types

import databases
import supports
import configs


def get_points(user_id: int, scores: int) -> int:
    """
    Функция прибавляет к текущему количеству очков пользователя заработанные за победу над монстром и проверяет,
    какому уровню соответствует новое количество очков. Если получен новый уровень, уведомляет пользователя.
    :param user_id: Уникальный ID пользователя в Телеграм
    :param scores: Очки за победу над монстром
    :return: Новое значение очков и уроня
    """
    user_data = supports.get_user_info(user_id)
    current_points = user_data['points']
    current_level = user_data['level']
    new_level = current_level
    new_points = current_points + scores
    for level in configs.levels_table.keys():
        if new_points in configs.levels_table[level]:
            new_level = level
    return new_points, new_level


def get_trophies(user_id: int, trophy: int, bot: telebot.TeleBot, message: any):
    """
    Функция выбирает тип сокровища, которое получит пользователь и добавляет его в профиль пользователя
    :param user_id: Уникальный ID пользователя в Телеграм
    :param trophy: Количество получаемых сокровищ
    :param bot: Объект сессии Телеграм
    :param message: Блок с данными о сообщении
    :return:
    """
    user_data = supports.get_user_info(user_id)
    while trophy != 0:
        db_name = random.choice(['coins_data', 'races_classes_data', 'things_data'])
        trophy = databases.get_trophy(db_name)
        if db_name == 'coins_data':
            current_coins = user_data['coins']
            new_coins = current_coins + trophy[2]
            databases.update_coins(user_id, new_coins)
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Ты открыл сундук, а там {trophy[1]} '
                     f'Ты получаешь <b>{trophy[2]}</b> монет 🪙',
                parse_mode='HTML'
            )
        elif db_name == 'races_classes_data':
            type_race_class = trophy[1]
            new_race_class = trophy[2]
            databases.update_race_class(user_id, type_race_class, new_race_class)
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Ты получил расу/класс <b>{trophy[2]}</b>\n'
                     f'{trophy[3]}',
                parse_mode='HTML'
            )
        else:
            databases.update_inventory(trophy)
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Ты получил вещь <b>{trophy[1]}</b>\n'
                     f'{trophy[3]}',
                parse_mode='HTML'
            )




