from aiogram.dispatcher.filters import BoundFilter
from loader import types


class isPrivate(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type == types.ChatType.PRIVATE


class isGroup(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type == types.ChatType.GROUP or message.chat.type == types.ChatType.SUPERGROUP
