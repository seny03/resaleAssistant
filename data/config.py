import os
import re
import configparser

configfile = configparser.RawConfigParser()
configfile.read('./data/config.cfg')

_regex_chat_id = r'\d{5,}'

# TOKEN
TOKEN = os.environ[configfile['bot']['token_var']]

# DATABASE (dataset)
DATABASE_FILENAME = configfile['data']['database']
BACKUP_PATH = configfile['data']['backup_path']
BACKUP_DB_PATTERN = configfile['data']['backup_database_pattern']
BACKUP_QUANTITY = int(configfile['data']['backup_quantity'])
BACKUP_PER_DAY = int(configfile['data']['backups_per_day'])
DATABASE_CSV = configfile['data']['csv']
DB_INIT_FILE = configfile['data']['init_database']

# ADMINS
USER_ID = set(map(int, re.findall(_regex_chat_id, configfile['markOutBot']['user_id'])))
DB_ACCESS_ID = set(map(int, re.findall(_regex_chat_id, configfile['markOutBot']['db_access_id'])))
ADMIN_ID = set(map(int, re.findall(_regex_chat_id, configfile['markOutBot']['admin_id'])))

# PARSER
LINK_HEAD = configfile['parser']['link_head']

# LOG
LOG_CONFIGFILE = configfile['log']['configfile']
