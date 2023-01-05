import sqlite3
import requests
import pandas as pd
import bs4
import re
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')
head_offer_link = config['parser']['link_head']


class Database:
    def __init__(self):
        global config
        self.config = config['data']
        self.conn = sqlite3.connect(self.config['database'])
        self.cur = self.conn.cursor()
        # init database
        self.cur.executescript(open(self.config['init_database'], 'r').read())

    def get_offers(self):
        return self.cur.execute("SELECT * FROM OFFERS;").fetchall()

    def get_offer_by_id(self, id):
        return self.cur.execute("SELECT * FROM OFFERS WHERE id = (?)", (id,)).fetchall()

    def is_offer_exist(self, id):
        return bool(len(self.get_offer_by_id(id)))

    def add_offer(self, info, desired_price=None):
        if not self.is_offer_exist(info['id']):
            self.cur.execute("INSERT INTO OFFERS (id, description, cur_price, desired_price) VALUES (?, ?, ?, ?)",
                             (info['id'], info['description'], info['cur_price'], desired_price))
            self.conn.commit()
            return
        self.cur.execute("UPDATE OFFERS SET description=(?), cur_price=(?), desired_price=(?) WHERE id=(?)",
                         (info['description'], info['cur_price'], desired_price, info['id'],))
        self.conn.commit()

    def sql2csv(self):
        db_df = pd.read_sql_query("SELECT * FROM OFFERS", self.conn)
        db_df.to_csv(self.config['csv'], index=False)


def link2id(link):
    return int(re.findall(r'(\d+$)', link)[0])


def id2link(id):
    return f'{head_offer_link}{id}'


def parse_link(link):
    response = requests.get(link)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    info = {'description': '', 'id': link2id(link)}

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
            cur_price = float(''.join(re.findall(r'[0-9.,]', cur_price)))
            info['cur_price'] = round(cur_price + 0.001, 2)
    return info


if __name__ == '__main__':
    db = Database()
    while True:
        try:
            data = input(">>").split()
            if data[0].lower() == 'q': break
            link = data[0]
            desire_price = float(data[1])
            info = parse_link(link)
            db.add_offer(info, desire_price)
        except Exception as e:
            print(repr(e))
            break
    db.sql2csv()
