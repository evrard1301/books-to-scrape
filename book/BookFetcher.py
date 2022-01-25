import requests
import re
from bs4 import BeautifulSoup
from .Book import *


class BookFetcher:
    def __init__(self, page_url, session):
        self.page_url = page_url
        self.session = session
        self.html = self.session.get(self.page_url).content

    def exec(self):
        root = BeautifulSoup(self.html, 'html.parser')

        info = BookInfo(
            root.find_all('td')[0].text, # upc
            root.find('h1').text, # title
            root.find('div', id='product_description')
            .next_sibling.next_sibling.text, # description
            root.find('a', href=re.compile('category/books/')).text # category
        )

        nb_available_prefix = len('In stock (')
        nb_available_suffix = len(' available)')

        page = BookPage(
            self.page_url, # page url
            'http://books.toscrape.com/' +
            '/'.join(root.find('img')['src'].split('/')[2:]), # image_url
            int(root.find('p', class_='instock').text.strip()[
                nb_available_prefix : -nb_available_suffix
            ]), # number available
            root.find('p', class_='star-rating')['class'][1] # review rating
        )

        price = BookPrice(
            float(root.find_all('td')[2].text[1:]), # no tax price
            float(root.find_all('td')[3].text[1:]) # tax price
        )

        book = Book(info, page, price)

        return book
