from aiogram.dispatcher.filters import BoundFilter
from loader import types
from data import USER_ID


class isUser(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.id in USER_ID
