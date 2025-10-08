"""
Модуль отвечает за механику боя с монстром
"""
import time

import telebot
from gtts import gTTS

import databases
import literary_texts
import supports


# Из бд монстров выбираются все монстры с силой меньше или = уровень пользователя +25 (добавить 3 монстров в бд для теста) done
# Из них выбирается 1 рандомный монстр done
# Завести отдельный модуль для боя done
# Получаем из БД инвентаря пользователя все вещи get_user_inventory и считаем сумму бонуса надетых, получая общую силу героя done
# Сравниваем силу героя и силу монстра done
# Если равно, пишем пользователю, что силы равны и все решит случай (сучий), сейчас бог подземелий Аид кинет кубик и если выпадет от 4 и выше - герой победит done
# Кидаем кубик, получаем число, сообщаем результат пользователю done
# Используя шаблонизатор текста, делаем красивое описание/обзор боя курсивом и со свиточком смайликом. КАК ЭТО бЫЛО лучшие моменты и тд жирно
# генерим награду и опыт, пишем пользователю, что он заработал


def battle(user_id: int, user_name: str, user_level: int, bot: telebot.TeleBot, message: any):
    """
    Функция выбирает из БД Монстров случайного монстра, чей уровень не больше, чем уровень пользователя +25.
    Далее суммирует уровень пользователя и бонус от всех надетых вещей, сравнивает с уровнем монстра и отдает исход боя.
    :param user_id: Уникальный ID пользователя в Телеграм
    :param user_name: Имя пользователя
    :param user_level: Уровень пользователя
    :param bot: Объект сессии Телеграм
    :param message: Блок с данными о сообщении
    """
    monster = databases.get_monster(user_level)
    monster_data = supports.get_monster_info(monster)
    time.sleep(2)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Вы открыли дверь!\n'
             f'За ней вас ждет <b>{monster_data['monster_name']}</b> с силой <b>{monster_data['strength']}</b>\n'
             f'В бой!',
        parse_mode='HTML')
    general_user_power = user_level
    user_inventory = databases.get_user_inventory(user_id)
    user_weapon = 'кулак'
    time.sleep(3)
    bot.send_chat_action(message.chat.id, 'typing')
# TODO: СДЕЛАНО сделать функции нормализации данных для инвентаря и монстров аналогично get_user_info в модуле supports
    for thing in user_inventory:
        thing_data = supports.get_thing_info(thing)
        if thing_data['state_active']:
            general_user_power += thing_data['bonus']
        if thing_data['type'] == 'Оружие':
            user_weapon = thing_data['thing_name']

    if general_user_power > monster_data['strength']:
        user_win = True
    elif general_user_power == monster_data['strength']:
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Ваша сила и сила монстра равны <b>{general_user_power}</b>\n'
                 f'Поэтому призываем бога Подземного мира Аида, '
                 f'дабы он волей случая (сучьего) решил исход боя, бросив кости судьбы🎲\n'
                 f'Если выпадет четное число - победа ваша🎉, если нечетное - победа за монстром☠️',
            parse_mode='HTML')
        time.sleep(3)
        dice_roll = bot.send_dice(message.chat.id, '🎲')
        dice_value = dice_roll.dice.value
        time.sleep(2)
        bot.send_chat_action(message.chat.id, 'typing')
        if dice_value % 2 == 0:
            bot.send_message(message.chat.id, f'Выпало число {dice_value}. '
                                              f'Поздравляем, судьба сегодня благосклонна к тебе, ты победил!')
            user_win = True
        else:
            bot.send_message(message.chat.id, f'Выпало число {dice_value}. '
                                              f'Слышен злобный смех Аида. Ты проиграл!')
            user_win = False
    else:
        user_win = False
    if user_win:
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Ты победил!\n'
                 f'В награду ты получаешь:\n'
                 f'<b>{monster_data['trophy']}</b> сундуков с сокровищами\n'
                 f'<b>{monster_data['scores']}</b> очков опыта',
            parse_mode='HTML')
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Ты проиграл!\n'
                 f'{monster_data['escalation']}'
        )
    time.sleep(2)
    bot.send_chat_action(message.chat.id, 'typing')
    battle_description = literary_texts.create_text(user_name, user_weapon, monster_data['monster_name'],
                                                    monster_data['description'], user_win)
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Вот как это запишут в летописях 📜\n'
             f'{battle_description}'
    )
    battle_audio = gTTS(battle_description, lang='ru')
    battle_audio.save('audios/battle_audio.mp3')
    time.sleep(2)
    bot.send_chat_action(message.chat.id, 'upload_audio')
    bot.send_audio(
        chat_id=message.chat.id,
        audio='audios/battle_audio.mp3',
        caption='А вот как споют об этом барды 🪕'
    )

# TODO: СДЕЛАНО доделать модуль с битвами
# TODO: СДЕЛАНО показывать красивое описание итога битвы
# TODO: СДЕЛАНО показать в итоге, кто победил, из бд достать сокровища монстра, чтобы было видно
# TODO: СДЕЛАНО зарегистрироваться на гитхабе, НЕТ заполнить файл read.md (google)