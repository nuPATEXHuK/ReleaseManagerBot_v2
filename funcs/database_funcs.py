# -*- coding: utf-8 -*-
# pylint: disable=use-list-literal
# pylint: disable=use-dict-literal
from typing import List, Dict
from funcs.sqlighter import SQLighter
from funcs import config_loader as cfg

DB = SQLighter(cfg.get_db())
ADMIN = cfg.get_admin()
STAGES = ['role', 'voice', 'timer', 'fix', 'final']


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
    return None


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
    result = SQLighter.execute_with_data_one(DB, request)
    if not result:
        return 'Не получен параметр в связи с ошибкой БД. ' \
               'Обратитесь к администратору.'
    param = formate_one(str(result))
    return param


def get_status_by_code(code: str):
    request = f'SELECT status, stage FROM releases WHERE code = "{code}"'
    result = SQLighter.execute_with_data_one(DB, request)
    if not result:
        return []
    result_list = formate_one(str(result)).split(' ')
    return result_list


def get_active_releases_list() -> List[List]:
    releases_code = get_active_releases_code()
    release_list = list()
    for code in releases_code:
        request = ('SELECT name, stage, current_ep '
                   f'FROM releases WHERE code = "{code}"')
        release_info = formate_all(
            SQLighter.execute_with_data_one(DB, request))
        name = release_info[0].replace('_', ' ')
        status = release_info[1]
        cur_ep = release_info[2]
        release_list.append([name, status, cur_ep])
    return release_list


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
            'role_std_time': results[10],
            'role_current_time': results[11],
            'voice_std_time': results[12],
            'voice_current_time': results[13],
            'timer_std_time': results[14],
            'timer_current_time': results[15],
            'fix_std_time': results[16],
            'fix_current_time': results[17],
            'final_std_time': results[18],
            'final_current_time': results[19],
            'role_users': results[20],
            'voice_users': results[21],
            'timer_users': results[22],
            'admin': results[23],
            'release_time': results[24]}


def set_new_param_value(params: dict, code: str):
    request = 'UPDATE releases SET '
    for param in params:
        param_type = type(params[param])
        if param_type == str:
            if params[param] == 'NULL':
                request += f'{param} = {params[param]}, '
            else:
                request += f'{param} = "{params[param]}", '
        elif param_type == int:
            request += f'{param} = {params[param]}, '
        else:
            return 'Неизвестный тип параметра'
    request = request.strip()[:-1]
    request += f' WHERE code = "{code}"'
    result = SQLighter.execute_without_data(DB, request)
    if not result:
        return 'Релиз не добавлен в связи с ошибкой БД. ' \
               'Обратитесь к администратору.'
    return 'Релиз изменён'


def start_release(code: str, reset: bool):
    if int(get_param('fast', code)) == 1:
        time_release = cfg.get_alert_stages('fast')
    elif int(get_param('top', code)) == 1:
        time_release = cfg.get_alert_stages('top')
    else:
        time_release = cfg.get_alert_stages('standard')
    for index, stage in enumerate(STAGES):
        cur_std_time = get_param(f'{stage}_std_time', code)
        manual_time = False
        if cur_std_time == 'None':
            set_new_param_value({f'{stage}_std_time': time_release[index]},
                                code)
        else:
            manual_time = True
        cur_time = get_param(f'{stage}_current_time', code)
        if cur_time == 'None' or reset:
            if manual_time:
                set_new_param_value(
                    {f'{stage}_current_time': int(cur_std_time)}, code)
            else:
                set_new_param_value(
                    {f'{stage}_current_time': time_release[index]}, code)
    cur_stage = get_param('stage', code)
    if cur_stage == 'None' or reset:
        set_new_param_value({'stage': 'role',
                             'release_time': 10080}, code)
    cur_ep = int(get_param('current_ep', code))
    if cur_ep == 0:
        set_new_param_value({'current_ep': 1}, code)
    set_new_param_value({'status': 1}, code)


def stop_release(code):
    set_new_param_value({'status': 0}, code)


def get_code_from_all_releases():
    request = 'SELECT code FROM releases'
    codes = SQLighter.execute_with_data_all(DB, request)
    return codes


def new_ep(code: str):
    cur_ep = int(get_param('current_ep', code))
    max_ep_str = get_param('max_ep', code)
    max_ep = None
    if not max_ep_str == 'NULL':
        max_ep = int(max_ep_str)
    if cur_ep == max_ep:
        set_new_param_value({'status': 0}, code)
        return True
    release_time = int(get_param('release_time', code))
    for stage in STAGES:
        std_time = int(get_param(f'{stage}_std_time', code))
        if stage == 'role':
            set_new_param_value(
                {f'{stage}_current_time': std_time + release_time},
                code)
        else:
            set_new_param_value(
                {f'{stage}_current_time': std_time},
                code)
    set_new_param_value({'stage': 'role',
                         'current_ep': cur_ep + 1,
                         'release_time': release_time + 10080}, code)
    return False


def new_stage(cur_stage: str, code: str):
    stage_index = STAGES.index(cur_stage) + 1
    stage_new = STAGES[stage_index]
    set_new_param_value({'stage': stage_new,
                         f'{cur_stage}_current_time': 0}, code)
