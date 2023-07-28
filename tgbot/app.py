from loader import bot

if __name__ == '__main__':
    import filters
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=False)

