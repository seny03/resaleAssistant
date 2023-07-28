import re

import bs4
import requests


class SellerParser:
    def __init__(self):
        self.head = "https://funpay.com/user/"

    def link2id(self, link):
        return int(re.findall(r'(\d+$)', link)[0])

    def id2link(self, id):
        return f'{self.head}{id}'

    def parse_seller(self, link):
        info = {}
        response = requests.get(link)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')

        for tag in soup.find_all("div", class_="review-item-detail"):
            print(tag)
