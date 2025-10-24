"""
Модуль отвечает за получение пользователем бонусов при победе над монстром
"""
import random
import re

import telebot

import databases
import supports
import configs


def get_points(user_id: int, scores: int, bot: telebot.TeleBot, message: any) -> None:
    """
    Функция прибавляет к текущему количеству очков пользователя заработанные за победу над монстром и проверяет,
    какому уровню соответствует новое количество очков. Если получен новый уровень, уведомляет пользователя.
    :param user_id: Уникальный ID пользователя в Телеграм
    :param scores: Очки за победу над монстром
    :param bot: Объект сессии Телеграм
    :param message: Блок с данными о сообщении
    :return:
    """
    user_data = supports.get_user_info(user_id)
    current_points = user_data['points']
    current_level = user_data['level']
    new_points = current_points + scores
    databases.update_points(user_id, new_points)
    new_level = current_level
    for level in configs.levels_table.keys():
        if new_points in configs.levels_table[level]:
            new_level = level
    if new_level != current_level:
        databases.update_level(user_id, new_level)
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Ты получил новый уровень <b>{new_level}</b> 🎉',
            parse_mode='HTML'
        )


def get_trophies(user_id: int, trophy_number: int, bot: telebot.TeleBot, message: any):
    """
    Функция выбирает тип сокровища, которое получит пользователь и добавляет его в профиль пользователя
    :param user_id: Уникальный ID пользователя в Телеграм
    :param trophy_number: Количество получаемых сокровищ
    :param bot: Объект сессии Телеграм
    :param message: Блок с данными о сообщении
    :return:
    """
    user_data = supports.get_user_info(user_id)
    while trophy_number != 0:
        db_name = random.choice(['coins_data', 'races_classes_data', 'things_data'])
        trophy = databases.get_trophy(db_name)
        if db_name == 'coins_data':
            current_coins = user_data['coins']
            new_coins = current_coins + trophy[2]
            databases.update_coins(user_id, new_coins)
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Ты открыл сундук, а там <b>{trophy[1]}</b>\n'
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
            databases.add_thing(user_id, trophy)
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Ты получил вещь <b>{trophy[1]}</b>\n'
                     f'{trophy[3]}',
                parse_mode='HTML'
            )
        trophy_number -= 1


def get_escalation(user_id: int, escalation_id: int, escalation: str, bot: telebot.TeleBot, message: any):
    """
    Функция получает описание и тип эскалации в виде числа, и в зависимости от него отнимает у пользователя
    очки, уровни, монеты или вещи.
    :param user_id: Уникальный ID пользователя в Телеграм
    :param escalation_id: Тип эскалации, обозначенный числом
    :param escalation: Тестовое описание эскалации
    :param bot: Объект сессии Телеграм
    :param message: Блок с данными о сообщении
    :return:
    """
    user_data = supports.get_user_info(user_id)
    if escalation_id == 1:
        minus_points = re.search(r'\d+', escalation)
        minus_points = int(minus_points.group())
        current_points = user_data['points']
        current_level = user_data['level']
        new_points = current_points - minus_points
        databases.update_points(user_id, new_points)
        new_level = current_level
        for level in configs.levels_table.keys():
            if new_points in configs.levels_table[level]:
                new_level = level
        if new_level != current_level:
            databases.update_level(user_id, new_level)
    elif escalation_id == 2:
        minus_level = re.search(r'\d+', escalation)
        minus_level = int(minus_level.group())
        current_level = user_data['level']
        new_level = current_level - minus_level
        databases.update_level(user_id, new_level)
    elif escalation_id == 3:
        minus_coins = re.search(r'\d+', escalation)
        minus_coins = int(minus_coins.group())
        current_coins = user_data['coins']
        new_coins = current_coins - minus_coins
        databases.update_coins(user_id, new_coins)
    else:
        del_thing_name = databases.lose_thing(user_id)
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Ты потерял вещь <b>{del_thing_name}</b>',
            parse_mode='HTML'
        )

# TODO: сделать функцию получения эскалаций - сделать проверку на меньше нуля!


