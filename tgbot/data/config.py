import os
import re

_regex_admin = r'\d{5,}'
ADMIN_ID = set(map(int, re.findall(_regex_admin, os.environ["ADMIN_ID"])))
TOKEN = os.environ["TOKEN"]
