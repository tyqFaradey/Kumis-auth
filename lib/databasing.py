from datetime import date
import lib.helper as helper
import sqlite3




class DataBase:
    def __init__(self):
        self.database_path = helper.get_path_database()
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (user_id TEXT PRIMARY KEY, 
                           user_nickname TEXT UNIQUE,
                           user_nickname_cash TEXT,
                           date TEXT,
                           tg_username_hash TEXT)''')
            conn.commit()

            cursor.execute(f"PRAGMA table_info(users)")

            self.column_names_arr = [column[1] for column in cursor.fetchall()]
            self.column_names_str = ", ".join(self.column_names_arr)



    def insert_user(self, values: tuple) -> int:
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()

            cursor.execute(f"INSERT INTO users ({self.column_names_str}) VALUES ({", ".join(["?"] * len(self.column_names_arr))})",
                           values)
            
            conn.commit()

    def modify_user(self, user_id: str, nickname: str, username_hash) -> None:
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()

            cursor.execute("UPDATE users SET user_nickname = ?, tg_username_hash = ?, date = ?, user_nickname_cash = ? WHERE user_id = ?", 
                                            (nickname, username_hash, date.today(), self.get_nickname(user_id), user_id))
            
            conn.commit()
    
    def dlete_user(self, user_id: str) -> None:
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()

            cursor.execute(f"DELETE FROM users WHERE {self.column_names_arr[0]} = ?", (user_id,))
            
            conn.commit()


    def nickname_is_in(self, user_id: str) -> int:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()

                cursor.execute(f"SELECT user_nickname FROM users WHERE user_id = ?", (user_id,))

                result = cursor.fetchone()
            return 200 if result[0] != None else 204

    def id_is_in(self, user_id) -> int:
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()

            cursor.execute(f"SELECT EXISTS(SELECT 1 FROM users WHERE user_id = ?)", (user_id,))

            exists = cursor.fetchone()[0]
        return bool(exists)


    def get_all_nicknames(self) -> list:
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()

            cursor.execute(f"SELECT user_nickname FROM users")

        return [item[0] for item in cursor.fetchall()]

    
    def get_values_by_value(self, values: tuple, by_name: str, by_value: str) -> tuple:
        result = ()
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            print(type(values))
            for val in (values,) if type(values) != "tuple" else values:
                
                cursor.execute(f"SELECT {val} FROM users WHERE {by_name} = ?", (by_value,))
                result += cursor.fetchall()[0]

        return result

    def get_nickname(self, user_id: str) -> str:
        return self.get_values_by_value("user_nickname", "user_id", user_id)[0]
    def get_date(self, user_id: str) -> str:
        return self.get_values_by_value("date", "user_id", user_id)[0]
    def get_username_hash_by_nick(self, nickname:str) -> str:
        return self.get_values_by_value("tg_username_hash", "user_nickname", nickname)[0]







#d = DataBase()

#d.insert_user(("3457543", "Dallix", None, "un5twewutnhwt5fuhwyf58hmuywf9hmuywf4hm", "12-12-12"))
#d.insert_user(("343", "qqq", None, "un5twewutnhwt5fuhwyf58hmuywf9hmuywf4hm", "12-12-12"))
#d.modify_user("343", ("11", "None", "un5twewutnhwt5fuhwyf58hmuywf9hmuywf4hm", "12-12-12"))
#print(d.get_all_nicknames())

#print(d.nickname_is_in("343"))
#print(d.id_is_in("3457543"))

#print(d.get_nickname("1334411"))



