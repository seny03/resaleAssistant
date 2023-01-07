import asyncio
import time
import validators
import configparser
import logging
import logging.config

from aiogram import Bot, Dispatcher, executor, types

from bot_config import *
from database import Database
from offer_parser import Parser


# parse config
conf = configparser.ConfigParser()
conf.read('config.cfg')
head_link = conf['parser']['link_head']
logging.config.fileConfig(conf['log']['configfile'])
logger = logging.getLogger('bot')

# bot init
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# init
db = Database()
parser = Parser()

startup_time = time.time()
offers_from_user = {x: 0 for x in ADMIN_ID}


async def warning(chat_id, username=None):
    await bot.send_message(chat_id, f"[!] Sorry, you don't have a permission to this bot. Your chat_id is {chat_id} !")
    logger.warning(f"Logging attempt from wrong user chat_id={chat_id}, username={username}")


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


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    # print(f'cur time: {startup_time}')
    # print(f'mes time: {(message.date.timestamp())}')
    chat_id = message.chat.id
    if chat_id not in ADMIN_ID:
        return await warning(chat_id, message.chat.username)
    await bot.send_message(chat_id, "[+] Successfully connected!")
    logger.debug(f"Successful login attempt from chat_id={chat_id}, username={message.chat.username}")


@dp.message_handler(commands='get_database')
async def get_db_command(message: types.Message):
    if message.chat.id not in DB_ACCESS_ID:
        await bot.send_message(message.chat.id,
                               f"[!] You dont have access to this feature! Your chat_id is {message.chat.id}")
        logger.warning(f"Access to DB. Permission denied chat_id={message.chat.id}")
        return
    file = types.InputFile(conf['data']['database'])
    await bot.send_document(message.chat.id, file, protect_content=True)
    logger.info(f"Access to DB chat_id={message.chat.id}. DB has been sent!")


@dp.message_handler(commands='get_csv')
async def get_db_command(message: types.Message):
    if message.chat.id not in DB_ACCESS_ID:
        await bot.send_message(message.chat.id,
                               f"[!] You dont have access to this feature! Your chat_id is {message.chat.id}")
        logger.warning(f"Access to DB. Permission denied chat_id={message.chat.id}")
        return
    db.sql2csv()
    await asyncio.sleep(1)
    file = types.InputFile(conf['data']['csv'])
    await bot.send_document(message.chat.id, file, protect_content=True)
    logger.info(f"Access to DB chat_id={message.chat.id}. DB has been converted to CSV!")


@dp.message_handler()
async def get_message(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in ADMIN_ID:
        return await warning(chat_id, message.chat.username)
    mes = message.text.split()
    if len(mes) != 2:
        await message.reply("[!] Incorrect arguments")
        logger.warning(f'Incorrect arguments chat_id={chat_id}')
        return
    link, desired_price = mes
    desired_price = desired_price.replace(',', '.')
    if not validators.url(link) or head_link not in link:
        await message.reply("[!] Wrong link value")
        logger.warning(f'Wrong link value chat_id={chat_id}')
        return
    if not desired_price.replace('.', '', 1).isdigit():
        await message.reply("[!] Wrong price value")
        logger.warning(f'Wrong price value chat_id={chat_id}')
        return

    await add_offer(link, float(desired_price))
    await send_answer(chat_id)
    return


if __name__ == "__main__":
    logger.warning("Starting bot")
    executor.start_polling(dp, skip_updates=False)
