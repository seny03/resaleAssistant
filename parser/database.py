import os
import time

import mysql.connector
from mysql.connector import connect, Error


class Database:
    def __init__(self):
        while True:
            try:
                self.db = connect(
                    host=os.environ["MYSQL_HOST"],
                    port=int(os.environ["MYSQL_PORT"]),
                    user="root",
                    password=os.environ["MYSQL_ROOT_PASSWORD"],
                    database=os.environ["MYSQL_DATABASE"]
                )
                break
            except:
                time.sleep(200/1000)
        self.cur = self.db.cursor()
        # init script
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Board (
  id INT PRIMARY KEY NOT NULL,
  description TEXT NOT NULL,
  price FLOAT NOT NULL,
  seller_link TEXT NOT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;""")
        self.db.commit()

    def add_offer(self, info):
        try:
            sql_query = "INSERT INTO Board VALUES (%s, %s, %s, %s);"
            data_tuple = (info['id'], info['description'], info["cur_price"], info["seller_link"])

            self.cur.execute(sql_query, data_tuple)
            self.db.commit()
            return True
        except Exception as e:
            return repr(e)

    def clear(self):
        self.cur.execute("DELETE FROM Board;")
        # self.db.commit()
