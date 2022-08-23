import sqlite3
from datetime import datetime


class SQLighter:

    # Инициирование подключения к БД
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_user_by_username(self, username: str):
        with self.connection:
            try:
                user = self.cursor.execute("SELECT user_id "
                                           "FROM users WHERE "
                                           f'nickname="{username}"').fetchone()
                return user
            except:
                return None

    # Закрытие подключения к БД
    def close(self):
        self.connection.close()
