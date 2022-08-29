# -*- coding: utf-8 -*-
from typing import List, Dict
from funcs.sqlighter import SQLighter
from funcs import config_loader as cfg

DB = SQLighter(cfg.get_db())
ADMIN = cfg.get_admin()


def formate_one(result: str):
    return result.replace('(', '').replace(')', '').replace(
        '\'', '').replace(',', '')


def formate_all(results: list):
    result_list = list()
    for result in results:
        result_list.append(formate_one(str(result)))
    return result_list


def add_release(chat_id: int, code: str):
    request = 'INSERT INTO releases (chat_id, code, name, admin_users) ' \
              f'VALUES ({chat_id}, "{code}", "{code}", "{ADMIN}")'
    result = SQLighter.execute_without_data(DB, request)
    if not result:
        return 'Релиз не добавлен в связи с ошибкой БД. ' \
               'Обратитесь к администратору.'


def get_release_code_by_chat(chat_id):
    request = f'SELECT code FROM releases WHERE chat_id = {chat_id}'
    result = str(SQLighter.execute_with_data_one(DB, request))
    if not result:
        return 'Не получен код релиза в связи с ошибкой БД. ' \
               'Обратитесь к администратору.'
    release_code = formate_one(result)
    return release_code


def get_param(param_name, code):
    request = f'SELECT {param_name} FROM releases WHERE code = "{code}"'
    result = str(SQLighter.execute_with_data_one(DB, request))
    if not result:
        return 'Не получен параметр в связи с ошибкой БД. ' \
               'Обратитесь к администратору.'
    param = formate_one(result)
    return param


def get_status_by_code(code: str) -> List:
    return []


def get_chat_id_by_code(code: str):
    return 0


def get_active_releases_list() -> List[List]:
    return []


def get_active_releases_code() -> List:
    request = 'SELECT code FROM releases WHERE status = 1'
    releases = formate_all(SQLighter.execute_with_data_all(DB, request))
    return releases


def get_release_data_by_code(code: str) -> Dict:
    request = f'SELECT * FROM releases WHERE code = "{code}"'
    release_data = SQLighter.execute_with_data_one(DB, request)
    if not release_data:
        return dict()
    results = formate_one(str(release_data)).split(' ')
    return {'chat_id': results[1],
            'name': results[3],
            'status': results[4],
            'stage': results[5],
            'fast': results[6],
            'top': results[7],
            'current_ep': results[8],
            'max_ep': results[9],
            'role_delta_time': results[10],
            'role_current_time': results[11],
            'voice_delta_time': results[12],
            'voice_current_time': results[13],
            'timer_delta_time': results[14],
            'timer_current_time': results[15],
            'fix_delta_time': results[16],
            'fix_current_time': results[17],
            'final_delta_time': results[18],
            'final_current_time': results[19],
            'role_users': results[20],
            'voice_users': results[21],
            'timer_users': results[22],
            'admin': results[23]}


def set_new_param_value(params: dict, code: str):
    request = 'UPDATE releases SET '
    for param in params:
        param_type = type(params[param])
        if param_type == str:
            request += f'{param} = "{params[param]}" '
        elif param_type == int:
            request += f'{param} = {params[param]} '
        else:
            return 'Неизвестный тип параметра'
    request += f'WHERE code = "{code}"'
    result = SQLighter.execute_without_data(DB, request)
    if not result:
        return 'Релиз не добавлен в связи с ошибкой БД. ' \
               'Обратитесь к администратору.'


def start_release(code):
    pass


def stop_release(code):
    pass
