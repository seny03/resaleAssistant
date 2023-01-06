import sqlite3
import pandas as pd
import configparser
import logging
import logging.config


class Database:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')
        self.config_db = self.config['data']

        logging.config.fileConfig(self.config['log']['configfile'])
        self.logger = logging.getLogger('db')

        self.conn = sqlite3.connect(self.config_db['database'])
        self.cur = self.conn.cursor()
        self.logger.debug(f"Connected to database {self.config_db['database']}")
        # init database
        self.cur.executescript(open(self.config_db['init_database'], 'r').read())
        self.conn.commit()
        self.logger.debug(f"Executed init script")

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
            self.logger.debug(f"UPDATE offer id={info['id']}")
            return
        self.cur.execute("UPDATE OFFERS SET description=(?), cur_price=(?), desired_price=(?) WHERE id=(?)",
                         (info['description'], info['cur_price'], desired_price, info['id'],))
        self.conn.commit()
        self.logger.debug(f"NEW offer id={info['id']}")

    def sql2csv(self):
        db_df = pd.read_sql_query("SELECT * FROM OFFERS", self.conn)
        db_df.to_csv(self.config_db['csv'], index=False)
        self.logger.info(f"Database converted to csv {self.config_db['csv']}")

    def backup(self):
        def progress(status, remaining, total):
            self.logger.warning(f'BACKUP copied {total - remaining} of {total} pages...')

        bck = sqlite3.connect(self.config_db['backup_database'])
        with bck:
            self.conn.backup(bck, pages=1, progress=progress)
        bck.close()
        self.logger.info(f"Database has been backedup to {self.config_db['backup_database']}")
