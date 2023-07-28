from loader import dp

# chat
from .chat import *
dp.filters_factory.bind(isPrivate)
dp.filters_factory.bind(isGroup)

# admin
from .admin import *
dp.filters_factory.bind(isAdmin)
