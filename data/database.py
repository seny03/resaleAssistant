import sqlite3
import pandas as pd
import logging
import logging.config
from datetime import datetime
import time
from .config import *


class Database:
    def __init__(self):
        logging.config.fileConfig(LOG_CONFIGFILE)
        self.logger = logging.getLogger('db')

        self.conn = sqlite3.connect(DATABASE_FILENAME)
        self.cur = self.conn.cursor()
        self.logger.debug(f"Connected to database {DATABASE_FILENAME}")
        # init database
        self.cur.executescript(open(DB_INIT_FILE, 'r').read())
        self.conn.commit()
        self.logger.debug(f"Executed init script")

    def get_offers(self):
        return self.cur.execute("SELECT * FROM OFFERS;").fetchall()

    def get_stats(self):
        stats = {}
        stats['quantity'] = len(self.get_offers())
        stats['price'] = {'max_price': 0, 'min_price': 0, 'mean_price': 0, 'good_deals': 0}
        prices = list(map(lambda x: float(x[0]), self.cur.execute("SELECT desired_price FROM OFFERS;").fetchall()))
        stats['quantity'] = len(prices)
        stats['price']['max_price'] = max(prices)
        stats['price']['min_price'] = min(prices)
        stats['price']['mean_price'] = sum(prices) / len(prices)
        for s, d in self.cur.execute("SELECT cur_price, desired_price FROM OFFERS;").fetchall():
            if d-s > d*0.15:
                stats['price']['good_deals'] += 1
        descriptions = list(map(lambda x: x[0], self.cur.execute("SELECT description FROM OFFERS;").fetchall()))
        stats['desc'] = {'max_length': 0, 'min_length': 0, 'mean_length': 0}
        lengths = list(map(lambda x: len(x), descriptions))
        stats['desc']['max_length'] = max(lengths)
        stats['desc']['min_length'] = min(lengths)
        stats['desc']['mean_length'] = sum(lengths) / len(lengths)
        return stats

    def get_offer_by_id(self, id):
        return self.cur.execute("SELECT * FROM OFFERS WHERE id = (?)", (id,)).fetchall()

    def is_offer_exist(self, id):
        return bool(len(self.get_offer_by_id(id)))

    def time2timestamp(self):
        timestamp = time.time()
        date_time = datetime.fromtimestamp(timestamp)
        str_date_time = date_time.strftime(DB_TIMESTAMP_FORMAT)
        return str_date_time

    def timestamp2time(self, timestamp):
        return datetime.timestamp(datetime.strptime(timestamp, DB_TIMESTAMP_FORMAT))

    def add_offer(self, info, desired_price=None):
        if not self.is_offer_exist(info['id']):
            self.cur.execute("INSERT INTO OFFERS (id, description, cur_price, desired_price, owner, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                             (info['id'], info['description'], info['cur_price'], desired_price, info['chat_id'], self.time2timestamp()))
            self.conn.commit()
            self.logger.debug(f"NEW offer id={info['id']} by chat_id={info['chat_id']}")
            return
        self.cur.execute("UPDATE OFFERS SET description=(?), cur_price=(?), desired_price=(?), owner=(?), timestamp=(?) WHERE id=(?)",
                         (info['description'], info['cur_price'], info['chat_id'], self.time2timestamp(), desired_price, info['id'],))
        self.conn.commit()
        self.logger.debug(f"UPDATE offer id={info['id']}")

    def sql2csv(self):
        db_df = pd.read_sql_query("SELECT * FROM OFFERS", self.conn)
        db_df.to_csv(DATABASE_CSV, index=False)
        self.logger.info(f"Database converted to csv {DATABASE_CSV}")

    def check_backup(self):
        backs = os.listdir(BACKUP_PATH)
        backs_quantity = int(BACKUP_QUANTITY)
        if len(backs) >= backs_quantity:
            remove_files = sorted(backs, key=lambda x: os.path.getctime(BACKUP_PATH + x), reverse=True)[backs_quantity-1:]
            for f in remove_files:
                os.remove(BACKUP_PATH + f)

    def generate_backup_name(self):
        name = BACKUP_PATH + datetime.now().strftime(BACKUP_DB_PATTERN)
        return name

    def backup(self):
        def progress(status, remaining, total):
            self.logger.warning(f'BACKUP copied {total - remaining} of {total} pages...')
        self.check_backup()
        name = self.generate_backup_name()
        bck = sqlite3.connect(name)
        with bck:
            self.conn.backup(bck, pages=1000000000, progress=progress)
        bck.close()
        self.logger.info(f"Database has been backedup to {name}")
