# -*- coding: utf-8 -*-
import funcs.database_funcs as dbf


def release_chat_exist(chat_id):
    code = dbf.get_release_code_by_chat(chat_id)
    if code:
        return code
    else:
        return False


def release_code_exist(code):
    pass


def release_already_start(code):
    pass
