"""
Модуль отвечает за получение пользователем бонусов при победе над монстром
"""

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


