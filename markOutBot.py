import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types

from bot_config import *
from database import Database
from parser import Parser

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


async def warning(chat_id):
    await bot.send_message(chat_id, f"[!] Sorry, you don't have a permission to this bot. Your chat_id is {chat_id} !")


async def add_offer(link, desired_price):
    info = parser.parse_link(link)
    db.add_offer(info, desired_price)
    print(f"{info} {desired_price}")


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
    return await message.reply("[+] added", reply=False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    executor.start_polling(dp)
