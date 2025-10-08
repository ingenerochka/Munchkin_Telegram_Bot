"""
Модуль обработки логов
"""

import logging
import os

import configs


def setup_logging() -> None:
    """
    Функция создает папку и файл для записи логов, если их нет, и настраивает параметры логирования
    :return: None
    """
    os.makedirs(configs.log_dir, exist_ok=True)
    # Создаст папку с указанным именем, если ее нет
    log_format = (
        '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s')
    logging.basicConfig(
        level=configs.log_level,
        format=log_format,
        encoding='utf-8',
        handlers=[
            logging.FileHandler(fr'{configs.log_dir}\{configs.log_filename}'),
            logging.StreamHandler()
        ]
    )
    logging.info('Логирование настроено')