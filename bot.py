# -*- coding: utf-8 -*-
# pylint: disable=import-error
import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types

from Logger import logger
from funcs import config_loader as cfg
from funcs import main_funcs as mf

logging.basicConfig(level=logging.INFO)

TOKEN = cfg.get_token()
BOT = Bot(TOKEN)
DP = Dispatcher(BOT)
TIMEOUT = cfg.get_timeout()
TAGS = ['#role', '#voice', '#timer', '#fix', '#final']


@DP.message_handler(commands=['start'])
async def start(message: types.Message) -> None:
    """
    Запускается при первом запуске бота или при команде /start

    :param message: входящая команда /start
    """
    await message.answer('Бот контроля релизов активирован')


@DP.message_handler(commands=['test'])
async def test(message: types.Message) -> None:
    """
    Тестовая функция для отладки

    :param message: входящая команда /test
    """
    answer = mf.test_func()
    if answer:
        await message.answer(answer)
    else:
        await message.answer('Ничего не вернулось')


@DP.message_handler(commands=['release_add'])
async def release_add(message: types.Message) -> None:
    """
    Добавление нового релиза на отслеживание

    :param message: входящая команда /release_add с кодом релиза
    """
    chat_id = message.chat.id
    if int(chat_id) > 0:
        await message.answer('Работает только в группах')
    else:
        code = message.text.replace(
            '/release_add', '').replace(
            '@releases_manager_bot', '').strip()
        if len(code) < 1:
            await message.answer('Неверные параметры')
        else:
            answer = mf.add_release(chat_id, code)
            await message.answer(answer)


@DP.message_handler(commands=['release_start'])
async def release_start(message: types.Message) -> None:
    """
    Старт отслеживания релиза

    :param message: входящая команда /release_start с параметром обновления
    """
    if int(message.chat.id) > 0:
        await message.answer('Работает только в группах')
    else:
        param = message.text.replace(
            '/release_start', '').replace(
            '@releases_manager_bot', '').strip()
        if param:
            if param == 'reset':
                answer = mf.start_release(message.chat.id, True)
            else:
                answer = ('Неверный параметр. Используйте reset для сброса '
                          'текущего времени этапов релиза')
        else:
            answer = mf.start_release(message.chat.id, False)
        await message.answer(answer)


@DP.message_handler(commands=['release_stop'])
async def release_stop(message: types.Message) -> None:
    """
    Остановка отслеживания релиза

    :param message: входящая команда /release_stop
    """
    if int(message.chat.id) > 0:
        await message.answer('Работает только в группах')
    else:
        answer = mf.stop_release(message.chat.id)
        await message.answer(answer)


@DP.message_handler(commands=['release_status'])
async def release_status(message: types.Message) -> None:
    """
    Проверка активности релиза

    :param message: входящая команда /release_status
    """
    chat_id = message.chat.id
    if int(chat_id) > 0:
        await message.answer('Работает только в группах')
    else:
        answer = mf.get_release_status(chat_id)
        await message.answer(answer)


@DP.message_handler(commands=['edit_release'])
async def edit_release(message: types.Message) -> None:
    """
    Настройка релиза

    :param message: входящая команда /edit_release со списком параметров
    """
    chat_id = message.chat.id
    if int(chat_id) > 0:
        await message.answer('Работает только в группах')
    else:
        params = message.text.replace(
            '/edit_release', '').replace(
            '@releases_manager_bot', '').strip().split(' ')
        if len(params) < 1:
            await message.answer('Неверные параметры')
        else:
            params_dict = {
                'name': None,
                'code': None,
                'fast': None,
                'top': None,
                'current_ep': None,
                'max_ep': None,
                'role_std_time': None,
                'voice_std_time': None,
                'timer_std_time': None,
                'fix_std_time': None,
                'final_std_time': None
                }
            for param in params:
                for key in params_dict:
                    if param.startswith(f'{key}='):
                        params_dict[key] = param.replace(f'{key}=', '')
            answer = mf.edit_release_in_db(chat_id,
                                           params_dict)
            await message.answer(answer)


@DP.message_handler(commands=['edit_work_group'])
async def edit_work_group(message: types.Message) -> None:
    """
    Редактирование списка пользователей на релизе

    :param message: входящая команда /edit_work_group со списком параметров
    """
    chat_id = message.chat.id
    if int(chat_id) > 0:
        await message.answer('Работает только в чате')
    else:
        params = message.text.replace(
            '/edit_work_group', '').replace(
            '@releases_manager_bot', '').strip().split(' ')
        if len(params) < 1:
            await message.answer('Неверные параметры')
        else:
            params_dict = {
                'role_users': None,
                'voice_users': None,
                'timer_users': None,
                'admin_users': None,
                'fix_users': None,
                'final_users': None
                }
            for param in params:
                for key in params_dict:
                    if param.startswith(f'{key}='):
                        params_dict[key] = param.replace(f'{key}=', '')
            answer = mf.edit_work_group_in_db(chat_id,
                                              params_dict)
            await message.answer(answer)


@DP.message_handler(commands=['release_list'])
async def release_list(message: types.Message) -> None:
    """
    Получение списка активных релизов

    :param message: входящая команда /release_list
    """
    if int(message.chat.id) > 0:
        answer = mf.get_releases_list()
        await message.answer(answer)
    else:
        await message.answer('Работает только в личных сообщениях')


@DP.message_handler(commands=['help'])
async def bot_help(message: types.Message) -> None:
    """
    Получение справки

    :param message: входящая команда /bot_help
    """
    if int(message.chat.id) > 0:
        answer = mf.get_help()
        await message.answer(answer)
    else:
        await message.answer('Работает только в личных сообщениях')


# Прослушка сообщений
@DP.message_handler(content_types=['text'])
async def message_listener(message: types.Message) -> None:
    """
    Постоянная прослушка сообщений. В группах работает только при активной
    админке бота

    :param message: любой текст, отправляемый боту
    """
    chat_id = message.chat.id
    if int(chat_id) < 0:
        if '#' in message.text:
            for tag in TAGS:
                if tag in message.text:
                    answer = mf.new_tag(chat_id, tag.replace('#', ''))
                    if answer:
                        await message.answer(answer)


async def scheduler(wait_for: int) -> None:
    """
    Функция (шедулер). Активна постоянно, проверятся раз в заданное время

    :param wait_for: время кулдауна на проверку (должно делиться на 60)
    """
    while True:
        logger.debug('Проверка релизов')
        answers = mf.check_releases(int(wait_for / 60))
        if answers and len(answers) > 0:
            for answer in answers:
                await BOT.send_message(answer[0], answer[1])
        await asyncio.sleep(wait_for)


# Стартовая функция для запуска бота.
if __name__ == "__main__":
    logger.info('Создаём новый циклический ивент для запуска шедулера')
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler(TIMEOUT))
    logger.info('Начало прослушки и готовности ботом принимать '
                'команды (long polling)')
    executor.start_polling(DP, skip_updates=True)
