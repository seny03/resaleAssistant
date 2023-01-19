from loader import dp

# admin
from .admin import isAdmin
dp.filters_factory.bind(isAdmin)

# user
from .user import isUser
dp.filters_factory.bind(isUser)

# has db access
from .db_access import haveDbAccess
dp.filters_factory.bind(haveDbAccess)

