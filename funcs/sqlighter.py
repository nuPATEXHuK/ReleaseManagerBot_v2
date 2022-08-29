import sqlite3
from sqlite3 import Error
from Logger import logger


class SQLighter:

    # Инициирование подключения к БД
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def execute_without_data(self, request: str):
        with self.connection:
            try:
                self.cursor.execute(request)
                return True
            except Error as e:
                logger.error('Ошибка при выполнении запроса в БД:\n%s', e)
                return False

    def execute_with_data_one(self, request: str):
        with self.connection:
            try:
                data = self.cursor.execute(request).fetchone()
                return data
            except Error as e:
                logger.error('Ошибка при выполнении запроса в БД:\n%s', e)
                return None

    def execute_with_data_all(self, request: str):
        with self.connection:
            try:
                data = self.cursor.execute(request).fetchall()
                return data
            except Error as e:
                logger.error('Ошибка при выполнении запроса в БД:\n%s', e)
                return None

    # Закрытие подключения к БД
    def close(self):
        self.connection.close()
