"""
Модуль отвечает за механику боя с монстром
"""
import logging
import time

import telebot
from telebot import types
from gtts import gTTS

import databases
import literary_texts
import supports
import victories


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
    for thing in user_inventory:
        thing_data = supports.get_thing_info(thing)
        if thing_data['state_active']:
            general_user_power += thing_data['bonus']
        if thing_data['type'] == 'Оружие':
            user_weapon = thing_data['thing_name']
    logging.info('Получена информация об оружии пользователя')

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
                                              f'Поздравляем, судьба сегодня благосклонна к тебе!')
            user_win = True
        else:
            bot.send_message(message.chat.id, f'Выпало число {dice_value}. '
                                              f'Слышен злобный смех Аида.')
            user_win = False
    else:
        user_win = False
    logging.info('Произошел бой. Получена информация о результате')
    time.sleep(2)
    bot.send_chat_action(message.chat.id, 'typing')
    battle_description = literary_texts.create_text(user_name, user_weapon, monster_data['monster_name'],
                                                    monster_data['description'], user_win)
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Бой окончен!\n'
             f'Вот как это запишут в летописях 📜\n'
             f'{battle_description}',
        parse_mode='HTML'
    )
    logging.info('Отправлено текстовое описание боя')
    #battle_audio = gTTS(battle_description, lang='ru')
    #battle_audio.save('audios/battle_audio.mp3')
    #battle_audio = open(r'audios/battle_audio.mp3', 'rb')
    #time.sleep(2)
    #bot.send_chat_action(message.chat.id, 'upload_audio')
    #bot.send_audio(
        #chat_id=message.chat.id,
        #audio=battle_audio,
        #caption='А вот как споют об этом барды 🪕'
    #)
    #battle_audio.close()
    logging.info('Отправлено голосовое описание боя')
    if user_win:
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Ты победил!\n'
                 f'В награду ты получаешь:\n'
                 f'<b>{monster_data['trophy']}</b> сундуков с сокровищами\n'
                 f'<b>+ {monster_data['scores']}</b> очков опыта',
            parse_mode='HTML')
        new_points, new_level = victories.get_points(user_id, monster_data['scores'])
        databases.update_points(user_id, new_points)
        if new_level != user_level:
            databases.update_level(user_id, new_level)
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Ты получил новый уровень <b>{new_level}</b>',
                parse_mode='HTML'
            )
            bot.set_message_reaction(message.chat.id, message_id=message.id,
                                     reaction=[types.ReactionTypeEmoji("🎉")], is_big=True)
        victories.get_trophies(user_id, monster_data['trophy'], bot, message)

    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Ты проиграл монстру! Но можешь попробовать сбежать, беги со всех ног!'
        )
        time.sleep(2)
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Удастся вам сбежать или нет, решит бог Подземного мира Аид, бросив кости судьбы🎲\n'
                 f'Если выпадет число больше 5 - вы сможете улизнуть🎉, если нет - монстр вас догонит☠️',
            parse_mode='HTML')
        time.sleep(3)
        dice_roll = bot.send_dice(message.chat.id, '🎲')
        dice_value = dice_roll.dice.value
        time.sleep(2)
        bot.send_chat_action(message.chat.id, 'typing')
        if dice_value >= 5:
            bot.send_message(message.chat.id, f'Выпало число {dice_value}. '
                                              f'Поздравляем, тебе удалось сбежать от монстра!\n'
                                              'Ты не получаешь эскалации, но покидаешь Подземелье с пустыми руками')
            user_escape = True
        else:
            bot.send_message(message.chat.id, f'Выпало число {dice_value}. '
                                              f'О, нет! Монстр догоняет тебя, схватив за пятку!\n'
                                              f'Ты получаешь эскалацию: {monster_data['escalation']}')
            user_escape = False





# TODO: сделать механизм выбора случайного сундука из бд сокровищ
# TODO: сделать механизм добавления попавшегося сокровища в инвентарь, если это шмотка
# TODO: сделать прибавление попавшегося сокровища к монетам пользователя, если это монеты
# TODO: сделать механизм присвоения герою расы или класса, если они попались в сокровищах (если уже есть,
#  прошлые меняются на новые, старые затираются)