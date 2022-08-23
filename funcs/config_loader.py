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


def get_alert_stages(release_type: str) -> List:
    """
    Получение списка времени для алертов в зависимости от типа релиза

    :param release_type: тип релиза (standard, fast, top)
    :return: список времени для алертов
    """
    stages_str = config.get('release_settings', f'{release_type}_release_time')
    return stages_str.split(',')
