from loader import bot, dp, types, db, logger
from filters import isAdmin, isUser


@dp.message_handler(isUser(), commands=['start'])
async def start_command_admin(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "[+] Successfully connected!")
    logger.debug(f"Successful login attempt from chat_id={chat_id}, username={message.chat.username}")
    return
