"""
Модуль обработки колбеков инлайн-клавиатур
"""
import logging

import battles
import configs
import databases
import supports
import keyboards


def get_callback(bot, call, user_id) -> None:
    """
    Функция обрабатывает коллбеки инлайн-клавиатур
    :param bot: Данные бота
    :param call: Строка с коллбеком
    :param user_id: Уникальный ID пользователя в Телеграм
    :return:
    """
    if 'profile' == call.data:
        logging.info('Пользователь запросил информацию о профиле')
        user_data = supports.get_user_info(user_id)
        bot.send_message(
            chat_id=call.message.chat.id,
            text=f'Имя героя 🧑: <b>{user_data['hero_name']}</b>\n'
                 f'Уровень 🏆: <b>{user_data['level']}</b>\n'
                 f'Количество очков 🎯: <b>{user_data['points']}</b>\n'
                 f'Количество монет 💰: <b>{user_data['coins']}</b>\n'
                 f'Количество ключей 🗝: <b>{user_data['keys']}</b>\n'
                 f'Раса 🧝‍♂️: <b>{user_data['race']}</b>\n'
                 f'Класс ⚜️: <b>{user_data['hero_class']}</b>\n'
                 f'Титул 👑: <b>{user_data['title']}</b>\n',
            parse_mode='HTML'
        )
        return

    if 'inventory' == call.data:
        logging.info('Пользователь запросил свой инвентарь')
        bot.send_message(chat_id=call.message.chat.id,
                         text='Здесь хранится информация обо всех вещах в твоем инвентаре. '
                              'Чтобы посмотреть надетые на твоего героя вещи, нажми <b>Экипировка</b>. '
                              'Чтобы посмотреть остальные не надетые вещи, нажми <b>Остальной инвентарь</b>.',
                         reply_markup=keyboards.inventory_keyboard(),
                         parse_mode='HTML'
                         )
        return

    def create_message_inventory(call_data):
        """
        :param call_data: тип колбека ('equipment' или 'other')
        :return:
        """
        result_inventory = databases.get_user_inventory(user_id)

        # Определяем заголовок и нужное состояние в зависимости от колбека
        if call_data == 'equipment':
            bot.send_message(
                chat_id=call.message.chat.id,
                text='Твоя экипировка:'
            )
            target_state = True  # Показываем только надетые вещи
        if call_data == 'other':
            bot.send_message(
                chat_id=call.message.chat.id,
                text='Твои вещи про запас:'
            )
            target_state = False  # Показываем только ненадетые вещи

        for row_result_inventory in result_inventory:
            thing_id_for_call, thing_name, thing_type, description, bonus, state_active = row_result_inventory

            # Пропускаем предметы, которые не соответствуют нужному состоянию
            if state_active != target_state:
                continue

            if state_active:
                state_active_str = '✅ Да'
                keyboard = keyboards.putout_keyboard(thing_id_for_call)
            if not state_active:
                state_active_str = '❌ Нет'
                keyboard = keyboards.puton_keyboard(thing_id_for_call)

            bot.send_message(
                chat_id=call.message.chat.id,
                text=f'<b>{thing_name}</b>\n'
                     f'Тип ⚔️: {thing_type}\n'
                     f'Описание 📜: {description}\n'
                     f'Бонус к уровню ➕: {bonus}\n'
                     f'Надето 🫅: {state_active_str}\n',
                reply_markup=keyboard,
                parse_mode='HTML'
            )
        return

    # Вызов функции
    if (call.data == 'equipment') or (call.data == 'other'):
        create_message_inventory(call_data=call.data)

    if 'keys' == call.data:
        logging.info('Пользователь запросил информацию о количестве ключей')
        keys = supports.get_user_info(user_id)['keys']
        check, doors = supports.keys_checking(user_id)
        if check is True:
            bot.answer_callback_query(
                callback_query_id=call.id,
                text=f'Текущее количество ключей 🗝: {keys}\n'
                     f'Можно открыть дверей 🚪: {int(doors)}',
                show_alert=True
            )
        else:
            bot.answer_callback_query(
                callback_query_id=call.id,
                text=f'Текущее количество ключей 🗝: {keys}\n'
                     'Недостаточно ключей для открытия двери 😥',
                show_alert=True
            )
        logging.info('Пользователь получил информацию о количестве ключей')
        return

    if 'rules' == call.data:
        bot.send_message(
            chat_id=call.message.chat.id,
            text='Здесь будет информация о правилах игры "Инженерский манчкин"'
        )
        logging.info('Пользователь запросил правила')
        return

    if 'dungeon' == call.data:
        logging.info('Пользователь захотел войти в Офисное подземелье')
        check, doors = supports.keys_checking(user_id)
        if check is True:
            user_data = supports.get_user_info(user_id)
            databases.open_door(user_id, configs.keys_for_open_door)
            battles.battle(user_id, user_data['hero_name'], user_data['level'], bot, call.message)
        else:
            bot.answer_callback_query(
                callback_query_id=call.id,
                text='Недостаточно ключей для открытия двери 😥\n'
                     'Делайте заявки, чтобы получить ключи.',
                show_alert=True
            )
        return

    if ('puton' in call.data) or ('putout' in call.data):
        thing_str = call.data
        print(call.data)
        command, thing_id = thing_str.split('_')
        thing_id = int(thing_id)
        databases.change_thing_status(user_id, thing_id, command)
        if command == 'puton':
            bot.answer_callback_query(
                callback_query_id=call.id,
                text=f'Вещь надета!',
                show_alert=True
            )
        if command == 'putout':
            bot.answer_callback_query(
                callback_query_id=call.id,
                text=f'Вещь снята!',
                show_alert=True
            )

