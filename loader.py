import logging
import logging.config
import time
import asyncio

from data import config, database, offer_parser, LOG_CONFIGFILE, USER_ID
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.middlewares.logging import LoggingMiddleware

startup_time = time.time()
offers_from_user = {x: 0 for x in USER_ID}

bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
db = database.Database()
parser = offer_parser.Parser()
logging.config.fileConfig(LOG_CONFIGFILE)
logger = logging.getLogger('bot')


async def add_offer(link, desired_price):
    info = parser.parse_link(link)
    db.add_offer(info, desired_price)
    logger.debug(f"ADD offer {info['id']}")


async def send_answer(chat_id):
    offers_from_user[chat_id] += 1
    cur_offers_number = offers_from_user[chat_id]
    await asyncio.sleep(1)
    if offers_from_user[chat_id] == cur_offers_number:
        await bot.send_message(chat_id, f"[+] Successfully added {cur_offers_number} offer(s)!")
        logger.info(f"Successfully added {cur_offers_number} offer(s)")
        offers_from_user[chat_id] = 0


#
# logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
#                     # level=logging.INFO,
#                     level=logging.DEBUG,
#                     )
