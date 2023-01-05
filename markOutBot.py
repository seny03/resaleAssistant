import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types

from bot_config import *
from database import Database
from offer_parser import Parser

import time
import validators
import configparser

# parse config
conf = configparser.ConfigParser()
conf.read('config.cfg')
head_link = conf['parser']['link_head']

# bot init
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# init
db = Database()
parser = Parser()

startup_time = time.time()
offers_from_user = {x: 0 for x in ADMIN_ID}


async def warning(chat_id):
    await bot.send_message(chat_id, f"[!] Sorry, you don't have a permission to this bot. Your chat_id is {chat_id} !")


async def add_offer(link, desired_price):
    info = parser.parse_link(link)
    db.add_offer(info, desired_price)
    print(f"{info} {desired_price}")


async def send_answer(chat_id):
    offers_from_user[chat_id] += 1
    cur_offers_number = offers_from_user[chat_id]
    await asyncio.sleep(1)
    if offers_from_user[chat_id] == cur_offers_number:
        await bot.send_message(chat_id, f"[+] Successfully added {cur_offers_number} offers!")
        offers_from_user[chat_id] = 0


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    print(f'cur time: {startup_time}')
    print(f'mes time: {(message.date.timestamp())}')
    chat_id = message.chat.id
    if chat_id not in ADMIN_ID:
        return await warning(chat_id)
    return await bot.send_message(chat_id, "[+] Successfully connected!")


@dp.message_handler()
async def get_message(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in ADMIN_ID:
        return await warning(chat_id)
    mes = message.text.split()
    if len(mes) != 2:
        return await message.reply("[!] Incorrect arguments")
    link, desired_price = mes
    desired_price = desired_price.replace(',', '.')
    if not validators.url(link) or head_link not in link:
        return await message.reply("[!] Wrong link value")
    if not desired_price.replace('.', '', 1).isdigit():
        return await message.reply("[!] Wrong price value")

    await add_offer(link, float(desired_price))
    return await send_answer(chat_id)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    executor.start_polling(dp)
