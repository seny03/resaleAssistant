from aiogram.dispatcher.filters import BoundFilter
from loader import types
from data import DB_ACCESS_ID


class haveDbAccess(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.id in DB_ACCESS_ID
