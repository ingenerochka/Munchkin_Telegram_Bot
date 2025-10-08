"""
Модуль для настройки клавиатур, отображаемых в Телеграм
"""

from telebot import types


def menu_keyboard() -> types.InlineKeyboardMarkup:
    """
    Данная функция создает и передает клавиатуру Главного меню бота
    :return: Объект InlineKeyboardMarkup с кнопками
    """
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Профиль 👤', callback_data='profile')
    button2 = types.InlineKeyboardButton(text='Инвентарь 💼', callback_data='inventory')
    button3 = types.InlineKeyboardButton(text='Ключи 🗝', callback_data='keys')
    button4 = types.InlineKeyboardButton(text='Правила 📜', callback_data='rules')
    button5 = types.InlineKeyboardButton(text='Войти в Офисное подземелье 🚪', callback_data='dungeon')

    markup.add(button1, button2)
    markup.add(button3, button4)
    markup.add(button5)

    return markup


def inventory_keyboard() -> types.InlineKeyboardMarkup:
    """
    Функция создает и передает клавиатуру для разделения инвентаря на надетое на героя и остальной инвентарь
    :return: Объект InlineKeyboardMarkup с кнопками
    """
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Экипировка 🪖', callback_data='equipment')
    button2 = types.InlineKeyboardButton(text='Остальной инвентарь 🎒', callback_data='other')
    markup.add(button1, button2)
    return markup

def puton_keyboard(thing_id) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Надеть вещь', callback_data=f'puton_{thing_id}')
    markup.add(button1)
    return markup

def putout_keyboard(thing_id) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Снять вещь', callback_data=f'putout_{thing_id}')
    markup.add(button1)
    return markup