from loader import *
from data import LINK_HEAD
from filters import isAdmin, isUser, haveDbAccess
import validators


@dp.message_handler(isUser(), content_types=['text'])
async def get_message(message: types.Message):
    chat_id = message.chat.id
    mes = message.text.split()
    if len(mes) != 2:
        await message.reply("[!] Incorrect arguments")
        logger.warning(f'Incorrect arguments chat_id={chat_id}')
        return
    link, desired_price = mes
    desired_price = desired_price.replace(',', '.')
    if not validators.url(link) or LINK_HEAD not in link:
        await message.reply("[!] Wrong link value")
        logger.warning(f'Wrong link value chat_id={chat_id}')
        return
    if not desired_price.replace('.', '', 1).isdigit():
        await message.reply("[!] Wrong price value")
        logger.warning(f'Wrong price value chat_id={chat_id}')
        return
    await add_offer(link, float(desired_price), message.chat.id)
    await send_answer(chat_id)
    return
