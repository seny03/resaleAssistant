from loader import bot, dp, types, db, logger
import asyncio
from data import DATABASE_CSV, DATABASE_FILENAME
from filters import isAdmin, isUser, haveDbAccess


@dp.message_handler(haveDbAccess(),commands='get_database')
async def get_db_command(message: types.Message):
    file = types.InputFile(DATABASE_FILENAME)
    await bot.send_document(message.chat.id, file, protect_content=True)
    logger.info(f"Access to DB chat_id={message.chat.id}. DB has been sent!")


@dp.message_handler(haveDbAccess(), commands='get_csv')
async def get_csv_command(message: types.Message):
    db.sql2csv()
    await asyncio.sleep(1)
    file = types.InputFile(DATABASE_CSV)
    await bot.send_document(message.chat.id, file, protect_content=True)
    logger.info(f"Access to DB chat_id={message.chat.id}. DB has been converted to CSV!")
