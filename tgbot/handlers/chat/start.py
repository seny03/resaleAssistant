from loader import bot, dp, types
from filters import isAdmin, isPrivate


@dp.message_handler(isPrivate(), isAdmin(), commands=['start'])
async def start_command_admin(message: types.Message):
    await bot.send_message(message.chat.id, "Hello, ADMIN")


@dp.message_handler(isPrivate(), commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Hello, user")

