import sqlite3
import pandas as pd
import configparser


class Database:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')
        self.config_db = self.config['data']
        self.conn = sqlite3.connect(self.config_db['database'])
        self.cur = self.conn.cursor()
        # init database
        self.cur.executescript(open(self.config_db['init_database'], 'r').read())

    def get_offers(self):
        return self.cur.execute("SELECT * FROM OFFERS;").fetchall()

    def get_offer_by_id(self, id):
        return self.cur.execute("SELECT * FROM OFFERS WHERE id = (?)", (id,)).fetchall()

    def is_offer_exist(self, id):
        return bool(len(self.get_offer_by_id(id)))

    def add_offer(self, info, desired_price=None):
        if not self.is_offer_exist(info['id']):
            self.cur.execute("INSERT INTO OFFERS (id, description, cur_price, desired_price) VALUES (?, ?, ?, ?)",
                             (info['id'], info['description'], info['cur_price'], desired_price))
            self.conn.commit()
            return
        self.cur.execute("UPDATE OFFERS SET description=(?), cur_price=(?), desired_price=(?) WHERE id=(?)",
                         (info['description'], info['cur_price'], desired_price, info['id'],))
        self.conn.commit()

    def sql2csv(self):
        db_df = pd.read_sql_query("SELECT * FROM OFFERS", self.conn)
        db_df.to_csv(self.config_db['csv'], index=False)
