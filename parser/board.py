import bs4
import re
import requests


class BoardParser:
    def __init__(self):
        self.head_offer_link = "https://funpay.com/lots/offer?id="

    def link2id(self, link):
        return int(re.findall(r'(\d+$)', link)[0])

    def id2link(self, id):
        return f'{self.head_offer_link}{id}'

    def parse_link(self, link):
        response = requests.get(link)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        info = {'description': '', 'id': self.link2id(link)}

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

        for tag in soup.find_all("div", class_="media-user-name"):
            info["seller_link"] = tag.find("a").get("href")
        return info

    def get_lot_links(self, lot_link):
        response = requests.get(lot_link)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        offers = set(map(lambda x: x.get('href'), soup.find_all(name='a', class_='tc-item')))
        return offers


