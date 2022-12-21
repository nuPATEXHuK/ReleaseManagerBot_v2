# -*- coding: utf-8 -*-
import configparser
from pathlib import Path
from typing import List

config = configparser.ConfigParser()
config.read(Path.cwd() / 'data' / 'config.cfg')


def get_token() -> str:
    """
    Получение токена бота из конфига

    :return: токен бота
    """
    token = config.get('main', 'token')
    return token


def get_db() -> Path:
    """
    Получение название файла с БД из конфига

    :return: путь до файла БД
    """
    database_file_name = config.get('main', 'db_file')
    database = Path.cwd() / 'data' / database_file_name
    return database


def get_admin() -> str:
    """
    Получение ника админа бота

    :return: ник админа
    """
    admin = config.get('main', 'admin')
    return admin


def get_timeout() -> int:
    """
    Получение таймаута в секундах

    :return: таймаут в секундах
    """
    timeout = int(config.get('main', 'timeout'))
    return timeout


def get_sleep_bot_time() -> list:
    """
    Получение времени отсутствия уведомлений от бота

    :return: время начала и конца заглушки
    """
    times = config.get('main', 'sleep_bot_time')
    time_start = times.split('-')[0]
    time_stop = times.split('-')[1]
    return [time_start, time_stop]


def get_alert_stages(release_type: str) -> List:
    """
    Получение списка времени для алертов в зависимости от типа релиза

    :param release_type: тип релиза (standard, fast, top)
    :return: список времени для алертов
    """
    stages_str = config.get('release_settings', f'{release_type}_release_time')
    return stages_str.split(',')
