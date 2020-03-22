"""
    Class DBWork, for working with a database
"""
import os
import sqlite3
import settings


class DBWork:

    def __init__(self):
        self.name_db = settings.DB_NAME
        self.table_name = settings.TABLE_NAME
        self.table_name_stat = settings.TABLE_STAT
        self.connect = self.set_db()

    """
        Check is create db, return db connections
    """
    def set_db(self):
        cur_dir = os.getcwd()
        path_db = os.path.join(cur_dir, self.name_db)
        if not os.path.exists(path_db):
            try:
                conn = sqlite3.connect(path_db)
                cursor = conn.cursor()
                cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {self.table_name} (name_combination text, querys text,"
                    f" products text, categories text, status text, message text)")
                cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {self.table_name_stat} (last_name_combination text, id integer )")
                cursor.execute(f"INSERT INTO {self.table_name_stat} VALUES ('empty', 1)")
                conn.commit()
            except sqlite3.Error as e:
                print('Ошибка БД: ' + str(e))
        return sqlite3.connect(self.name_db, check_same_thread=False)

    def inser_data_sucsseful(self, combination, querys, products, categories, status, message):
        cursor = self.connect.cursor()
        cursor.execute(f"""INSERT INTO {self.table_name} VALUES(?, ?, ?, ?, ?, ?)""", (combination, querys, products,
                                                                                       categories, status, message))
        self.connect.commit()

    def insert_last_combinations(self, last_cmb):
        cursor = self.connect.cursor()
        cursor.execute(f"UPDATE '{self.table_name_stat}' SET last_name_combination = '{last_cmb}' WHERE id = 1")
        self.connect.commit()

    def get_last_combinations(self):
        cursor = self.connect.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name_stat} WHERE id = 1")
        return cursor.fetchone()
