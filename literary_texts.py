"""
Модуль для создания текстов описания боев из шаблонов
"""

import random


def create_text(hero_name: str, hero_weapon: str, monster_name: str, monster_description: str, user_win: bool):
    """
    Функция составляет литературное описание хода боя из случайных фраз
    :param hero_name: имя пользователя
    :param hero_weapon: оружие пользователя из инвентаря
    :param monster_name: имя монстра
    :param monster_description: описание монстра
    :param user_win: победил пользователь или нет в bool формате
    :return: текст описания боя
    """
    start_text = [
        f'Уверенный в себе герой <b>{hero_name}</b> 🧙 c ноги выбивает дверь🚪, но на него тут же прыгает '
        f'<b>{monster_name}</b>. Монстр 🐉 - {monster_description}, и наносит удар первым. ',
        f'Герой <b>{hero_name}</b> 🧙 осторожно открывает скрипучую дверь🚪, осматривается и видит ужасное чудовище🐉 -'
        f' это <b>{monster_name}</b>. Герой бросается в атаку, но <b>{monster_name}</b> отражает ее. '
        f'Монстр - {monster_description}. ',
        f'Наш доблестный герой <b>{hero_name}</b> 🧙 без страха входит в подземелье 🕸 и смотрит прямо в глаза 👀 '
        f'монстру, несмотря на то, что <b>{monster_name}</b> 🐉 - {monster_description}. Начинается бой. '

    ]
    sequel_text = [
        f'{hero_weapon} 🗡 нависает над монстром, пока <b>{hero_name}</b> элегантно замахивается. '
        f'<b>{monster_name}</b> не успевает увернуться и получает удар 💥 в грудь. ',
        f'<b>{monster_name}</b> скалит зубы 🦷, но получает по ним, ведь у героя есть {hero_weapon}. '
        f'<b>{hero_name}</b> ⚔️ бьет им по голове монстра. ',
        f'{hero_weapon} 🗡 помогает герою пустить крови монстра. <b>{hero_name}</b> 🤺 наносит удар, '
        f'а <b>{monster_name}</b> зализывает рану. '
    ]
    if user_win:
        final_text = [
            f'<b>{hero_name}</b> пронзает 🗡 монстра насквозь. <b>{monster_name}</b> остается с дырой в груди. '
            f'{hero_weapon} победно сверкает, пока с него стекает кровь 🩸',
            f'Голова монстра 🐲 падает к ногам героя. Его {hero_weapon} ⚔️ отлично сделал свою работу, '
            f'<b>{monster_name}</b> больше не поднимется. <b>{hero_name}</b> смахивает с себя капли крови 🩸',
            f'{hero_weapon} отрубает монстру ногу. <b>{monster_name}</b> скулит 💦 и прячется в угол, '
            f'а герой <b>{hero_name}</b> издает победный клич 🗯'
        ]
    else:
        final_text = [
            f'Но герой слишком радовался первому успеху. Минуту спустя <b>{monster_name}</b> кусает героя за 🥚 яйца. '
            f'<b>{hero_name}</b> истошно вопит 🗯 и убегает. Позор! 👎',
            f'Но чаша весов неожиданно склоняется в другу сторону. Через несколько минут <b>{monster_name}</b> издает '
            f'жуткий рев, раздающийся по подземелью 🦇, а <b>{hero_name}</b> 💀 валяется в крови рядом. '
            f'Бесславный конец 🪦',
            f'Однако первый удар не решает исход сражения, дальше все пошло не по плану. <b>{hero_name}</b> ☠️ старался'
            f' как мог, но не смог. <b>{monster_name}</b> яростно насилует героя в углу подземелья 🌚'
        ]
    full_text = random.choice(start_text) + random.choice(sequel_text) + random.choice(final_text)
    return full_text


def test():
    for _ in range(10):
        hero_name = random.choice(['Саша', 'Мария', 'Юлия', 'Кошко-девочка'])
        hero_weapon = random.choice(['Палка', 'Кулак', 'Нога', 'Меч', 'Булава', 'Когти'])
        monster_name = random.choice(['Крыса', 'Вампир', 'Дракониха'])
        monster_description = random.choice(['мелкая, но вредная тварь', 'невероятно быстр и силен, сексуален',
                                             'огнедышащая леди, один вздох и ты шашлычок'])
        user_win = random.choice([True, False])
        result = create_text(hero_name, hero_weapon, monster_name, monster_description, user_win)
        print(result)

#test()




