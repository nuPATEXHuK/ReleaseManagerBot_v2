# -*- coding: utf-8 -*-
import funcs.database_funcs as dbf


def release_chat_exist(chat_id):
    code = dbf.get_release_code_by_chat(chat_id)
    if code == 'None':
        return False
    else:
        return code


def release_code_exist(code):
    code_list = dbf.get_code_from_all_releases()
    for code_from_db in code_list:
        if dbf.formate_one(str(code_from_db)) == code:
            return True
    return False


def release_already_start(code):
    return bool(int(dbf.get_param('status', code)))
