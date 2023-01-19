from loader import *


if __name__ == '__main__':
    from aiogram import executor
    from data.config import *
    from handlers import dp
    import asyncio
    import time


    async def db_backuper(per_day=12):
        delay = 24 * 60 * 60 / per_day
        while True:
            db.backup()
            await asyncio.sleep(delay)

    async def on_startup(x):
        asyncio.create_task(db_backuper(BACKUP_PER_DAY))


    logger.warning("Starting bot")
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)

