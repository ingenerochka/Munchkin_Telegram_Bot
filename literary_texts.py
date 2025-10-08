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
        f'Уверенный в себе герой {hero_name} c ноги выбивает дверь, но на него тут же прыгает {monster_name}. '
        f'Монстр - {monster_description}, и наносит удар первым. ',
        f'Герой {hero_name} осторожно открывает скрипучую дверь, осматривается и видит ужасное чудовище - это {monster_name}. '
        f'Герой бросается в атаку, но {monster_name} отражает ее. Монстр - {monster_description}. ',
        f'Наш доблестный герой {hero_name} без страха входит в подземелье и смотрит прямо в глаза монстру, '
        f'несмотря на то, что {monster_name} - {monster_description}. Начинается бой. '

    ]
    sequel_text = [
        f'{hero_weapon} нависает над монстром, пока {hero_name} элегантно замахивается. '
        f'{monster_name} не успевает увернуться и получает удар в грудь. ',
        f'{monster_name} скалит зубы, но получает по ним, ведь у героя есть {hero_weapon}. '
        f'{hero_name} бьет им по голове монстра. ',
        f'{hero_weapon} помогает герою пустить крови монстра. {hero_name} наносит удар, '
        f'а {monster_name} зализывает рану. '
    ]
    if user_win:
        final_text = [
            f'{hero_name} пронзает монстра насквозь. {monster_name} остается с дырой в груди. '
            f'{hero_weapon} победно сверкает, пока с него стекает кровь.',
            f'Голова монстра падает к ногам героя. Его {hero_weapon} отлично сделал свою работу, '
            f'{monster_name} больше не поднимется. {hero_name} смахивает с себя капли крови.',
            f'{hero_weapon} отрубает монстру ногу. {monster_name} скулит и прячется в угол, '
            f'а герой {hero_name} издает победный клич.'
        ]
    else:
        final_text = [
            f'{monster_name} кусает героя за яйца. {hero_name} истошно вопит и убегает. Позор!',
            f'{monster_name} издает жуткий рев, раздающийся по подземелью, а {hero_name} валяется в крови рядом. '
            f'Бесславный конец.',
            f'{hero_name} старался как мог, но не смог. {monster_name} яростно насилует его в углу подземелья.'
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
# TODO: СДЕЛАНО исправить ошибки в текстах (склонения, пробелы и тд)



