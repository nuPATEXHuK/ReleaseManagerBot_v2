# -*- coding: utf-8 -*-
from typing import List, Dict
from funcs.sqlighter import SQLighter
from funcs import config_loader as cfg

DB = SQLighter(cfg.get_db())
ADMIN = cfg.get_admin()


def add_release(chat_id, code):
    pass


def get_release_code_by_chat(chat_id):
    pass


def get_param(param_name, code):
    pass


def get_status_by_code(code: str) -> List:
    return []


def get_chat_id_by_code(code: str):
    pass


def get_active_releases_list() -> List[List]:
    return []


def get_active_releases_code() -> List:
    return []


def get_release_data_by_code(code: str) -> Dict:
    return {}


def set_new_param_value(param_name, param_value, code):
    pass


def start_release(code):
    pass


def stop_release(code):
    pass
