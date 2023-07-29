from board import BoardParser
from database import Database
from cache import Cacher
from logger import Logger

p = BoardParser()
db = Database()
cacher = Cacher()
db.clear()
cacher.clear()
l = Logger()
l.clear()

c = 0
f = p.get_lot_links("https://funpay.com/lots/288/")
print(set(f), len(f))
print("\n"*5)
s = p.get_lot_links("https://funpay.com/lots/288/")
print(set(s), len(s))
exit()
for offer in p.get_lot_links("https://funpay.com/lots/288/"):
    parsed = p.parse_link(offer)
    cacher.add_offer(parsed)
    err = db.add_offer(parsed)
    if err is not True:
        l.log.warning(err)
    else:
        l.log.info(f"parsed added {p.id2link(parsed['id'])}")
    c += 1
    if c == 10:
        exit()
