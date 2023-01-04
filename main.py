import sqlite3
import requests
import pandas as pd
import bs4
import re

aspect_ratio = 1.1609


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.sqlite')
        self.cur = self.conn.cursor()
        # init database
        self.cur.executescript(open('init.sql', 'r').read())

    def get_offers(self):
        return self.cur.execute("SELECT * FROM OFFERS;").fetchall()

    def get_offer_by_link(self, link):
        return self.cur.execute("SELECT * FROM OFFERS WHERE link = (?)", (link,)).fetchall()

    def is_offer_exist(self, link):
        return bool(len(self.get_offer_by_link(link)))

    def add_offer_link(self, link, info, desired_price=None):
        if not self.is_offer_exist(link):
            self.cur.execute("INSERT INTO OFFERS (link, description, buy_price, sell_price, desired_price) VALUES (?, "
                             "?, ?, ?, ?)",
                             (link, info['description'], float(info['buy_price']), float(info['sell_price']),
                              desired_price))

            self.conn.commit()
            return
        self.cur.execute("UPDATE OFFERS SET description=(?), buy_price=(?), sell_price=(?), desired_price=(?) WHERE "
                         "link=(?)",
                         (info['description'], float(info['buy_price']), float(info['sell_price']), desired_price,
                          link,))
        self.conn.commit()

    def sql2csv(self, filename='export.csv'):
        db_df = pd.read_sql_query("SELECT * FROM OFFERS", self.conn)
        db_df.to_csv(filename, index=False)


def parse_link(link):
    response = requests.get(link)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    info = {'description': ''}
    # info['link'] = link
    for tag in soup.find_all(name='div', class_='param-item'):
        title = tag.find('h5').text
        text = tag.find('div').text
        if title in ['Краткое описание', 'Подробное описание']:
            info['description'] += text + '. '
    for tag in soup.find_all(name='div', class_='form-group'):
        for option in tag.find_all(name='option', class_='hidden'):
            data_content = option.get('data-content')
            data_content_soup = bs4.BeautifulSoup(data_content, 'html.parser')
            cur_price = data_content_soup.find(name='span', class_='payment-value').text
            # cur_price = float(''.join(re.findall('\d.', cur_price)))
            cur_price = float(''.join(re.findall(r'[^а-я₽\s]', cur_price)).replace(' ', ''))
            info['sell_price'] = round(cur_price / aspect_ratio + 0.001, 2)
            info['buy_price'] = round(cur_price + 0.001, 2)
    return info


if __name__ == '__main__':
    db = Database()
    while True:
        try:
            data = input(">>").split()
            link = data[0]
            desire_price = float(data[1])
            info = parse_link(link)
            db.add_offer_link(link, info, desire_price)
        except Exception:
            break
    db.sql2csv()
