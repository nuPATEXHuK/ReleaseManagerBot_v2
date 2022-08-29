# -*- coding: utf-8 -*-
from typing import Optional, List, Dict

import funcs.check_funcs as check
import funcs.database_funcs as dbf
from Logger import logger


def add_release(chat_id: int, code: str) -> str:
    """
    Добавление нового релиза в БД

    :param chat_id: ID чата, где вызвана команда
    :param code: уникальный код релиза
    :return: результат добавления или причина, почему релиз не добавлен
    """
    logger.info('Запущено добавление нового релиза с кодом %s', code)
    if check.release_chat_exist(chat_id):
        return 'Релиз этого чата уже существует'
    if check.release_code_exist(code):
        return 'Релиз с таким кодом уже существует'
    errors = dbf.add_release(chat_id, code)
    if not errors:
        logger.info('Релиз добавлен')
        return 'Релиз добавлен'
    else:
        return errors


def edit_release_in_db(chat_id: int, params_dict: dict) -> str:
    """
    Изменение параметров релиза, привязанного к чату

    :param chat_id: ID чата, где вызвана команда
    :param params_dict: параметры для изменения релиза
    :return: информация об изменённых параметрах релиза
    """
    if not check.release_chat_exist(chat_id):
        return 'Релиз, привязанный к этому чату, не найден'
    release_code = dbf.get_release_code_by_chat(chat_id)
    new_params = get_new_release_params_dict(params_dict, release_code)
    if not new_params:
        return 'Новые параметры релиза не заданы'
    dbf.set_new_param_value(new_params, release_code)
    return 'Релиз изменён'


def edit_work_group_in_db(chat_id: int, params_dict: dict) -> str:
    """
    Изменение списка пользователей по ролям, привязанных к релизу

    :param chat_id: ID чата, где вызвана команда
    :param params_dict: параметры для изменения ролей на релизе
    :return: информация об изменённом списке пользователей
    """
    if not check.release_chat_exist(chat_id):
        return 'Релиз, привязанный к этому чату, не найден'
    release_code = dbf.get_release_code_by_chat(chat_id)
    new_params = get_new_users_params_dict(params_dict, release_code)
    if not new_params:
        return 'Новые пользователи в группах не заданы'
    for param in new_params.keys():
        dbf.set_new_param_value(new_params, release_code)
    return 'Рабочая группа релиза изменена'


def start_release(chat_id: int) -> str:
    """
    Запуск релиза в работу

    :param chat_id: ID чата, где вызвана команда
    :return: статус релиза
    """
    if not check.release_chat_exist(chat_id):
        return 'Релиз, привязанный к этому чату, не найден'
    release_code = dbf.get_release_code_by_chat(chat_id)
    if check.release_already_start(release_code):
        return 'Релиз уже запущен в работу'
    dbf.start_release(release_code)
    return 'Релиз запущен'


def stop_release(chat_id: int) -> str:
    """
    Остановка активности релиза с сохранением текущих параметров

    :param chat_id: ID чата, где вызвана команда
    :return: статус релиза
    """
    if not check.release_chat_exist(chat_id):
        return 'Релиз, привязанный к этому чату, не найден'
    release_code = dbf.get_release_code_by_chat(chat_id)
    if not check.release_already_start(release_code):
        return 'Релиз уже остановлен'
    dbf.stop_release(release_code)
    return 'Релиз запущен'


def get_release_status(chat_id: int) -> str:
    """
    Получение статуса релиза (активен или остановлен)

    :param chat_id: ID чата, где вызвана команда
    :return: статус релиза
    """
    if not check.release_chat_exist(chat_id):
        return 'Релиз, привязанный к этому чату, не найден'
    release_code = dbf.get_release_code_by_chat(chat_id)
    status = dbf.get_status_by_code(release_code)
    if status[0] != 'inactive':
        return f'Релиз в работе, текущий этап: {status[1]}'
    return 'Релиз остановлен'


def get_releases_list() -> str:
    """
    Получение списка активных релизов

    :return: список активных релизов или сообщение об их отсутствии
    """
    answer = 'Список активных релизов:\n'
    releases = dbf.get_active_releases_list()
    if len(releases) < 1:
        answer = 'Нет активных релизов'
    else:
        for release in releases:
            answer += f'•\t{release[0]}. Текущий этап: {release[1]}'
    return answer


def check_releases(wait_time: int) -> Optional[List[List]]:
    """
    Проверка всех активных релизов на срок сдачи (4 раза за этап работы)

    :param wait_time: таймаут шедулера в минутах
    :return: список релизов с сообщениями в них или None
    """
    active_releases_code = dbf.get_active_releases_code()
    if len(active_releases_code) < 1:
        return None
    answer = list()
    for code in active_releases_code:
        release_data = dbf.get_release_data_by_code(code)
        chat_id = int(release_data['chat_id'])
        stage = str(release_data['stage'])
        admin = str(release_data['admin'])
        std_delta_time = int(release_data[f'{stage}_delta_time'])
        stage_key = f'{stage}_current_time'
        cur_delta_time = int(release_data[stage_key])
        cur_delta_time -= wait_time
        dbf.set_new_param_value({stage_key: cur_delta_time}, code)
        step = std_delta_time / 4
        if cur_delta_time % step == 0 and cur_delta_time <= std_delta_time:
            users = str(release_data[f'{stage}_users']).split(' ')
            alert = ''
            if len(users) > 0:
                for user in users:
                    if user == 'None':
                        alert += f'@{admin}'
                    else:
                        alert += f'@{user} '
            else:
                alert += f'@{admin}'
            if cur_delta_time > 0:
                alert += f'\nДо конца срока этапа {stage} ' \
                         f'осталось: {round(cur_delta_time / 60, 2)} ч.'
            else:
                if len(users) > 0 and users[0] != 'None':
                    alert += f' @{admin}'
                if cur_delta_time == 0:
                    alert += f'\nЭтап {stage} просрочен!'
                else:
                    alert += f'\nЭтап {stage} просрочен! Просрочка ' \
                         f'составляет: {-round(cur_delta_time / 60, 2)} ч.'
            answer.append([chat_id, alert])
    if len(answer) < 1:
        return None
    return answer


def get_new_release_params_dict(params: dict,
                                release_code: str) -> Optional[Dict]:
    """
    Проверка и возврат новых параметров релиза (без незаполненных и одинаковых)

    :param params: список новых параметров релиза
    :param release_code: код релиза
    :return: список новых параметров или None
    """
    new_params = dict()
    for key in params.keys():
        new_param_value = params[key]
        if new_param_value:
            param_from_db = dbf.get_param(key, release_code)
            if param_from_db == new_param_value:
                continue
            else:
                if not (key == 'name' or key == 'code'):
                    if 'delta_time' in key:
                        new_params[key] = int(new_param_value) * 60
                    else:
                        new_params[key] = int(new_param_value)
                else:
                    new_params[key] = new_param_value
    if len(new_params) < 1:
        return None
    return new_params


def get_new_users_params_dict(params: dict,
                              release_code: str) -> Optional[Dict]:
    """
    Проверка и возврат новых пользователей на ролях релиза
    (без незаполненных и одинаковых)

    :param params: список новых пользователей по группам
    :param release_code: код релиза
    :return: список новых пользователей по группам или None
    """
    new_params = dict()
    for key in params.keys():
        new_param_value = params[key]
        if new_param_value:
            param_from_db = dbf.get_param(key, release_code)
            if param_from_db == new_param_value:
                continue
            else:
                user_list = str(new_param_value).split(',')
                new_users = ''
                for user in user_list:
                    new_users += user.strip().replace('@', '') + ','
                new_users = new_users.strip(',')
                new_params[key] = new_users
    if len(new_params) < 1:
        return None
    return new_params


def test_func():
    answer = dbf.get_release_data_by_code('test_release')
    if len(answer) > 0:
        return str(answer['test'])
    return answer
