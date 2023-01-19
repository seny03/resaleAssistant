from aiogram.dispatcher.filters import BoundFilter
from loader import types
from data import ADMIN_ID


class isAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.id in ADMIN_ID
