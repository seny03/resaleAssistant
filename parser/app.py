import os
import time

from board import BoardParser
from database import Database
from cache import Cacher
from logger import Logger

logger = Logger().log
cacher = Cacher()
logger.info("[!] Connected to REDIS successfully")
db = Database()
logger.info("[!] Connected to DB successfully")
board_parser = BoardParser()
TIMEOUT = int(os.environ["PARSE_TIMEOUT"])

# just for test
cacher.clear()
db.clear()


def parse_all(lot_link):
    logger.info(f"[!] Parsing started {lot_link}")
    links = board_parser.get_lot_links(lot_link)
    for link in links:
        info = board_parser.parse_link(link)
        # filter
        if info['cur_price'] > 20_000 or len(info['description']) < 100: continue
        db.add_offer(info)
        cacher.add_offer(info)
        time.sleep(200/1000)
        logger.info(f"[+] Item added id={info['id']}")


if __name__ == '__main__':
    while True:
        parse_all("https://funpay.com/lots/288/")
        time.sleep(TIMEOUT)
