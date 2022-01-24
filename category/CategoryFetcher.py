import requests
from bs4 import BeautifulSoup

from book import BookFetcher
from category import Category


class CategoryFetcher:
    def __init__(self, url):
        self.url = '/'.join(url.split('/')[:-1])
        self.root = BeautifulSoup(requests.get(self.url + '/' + 'index.html').content, 'html.parser')

        self.page_count = self.get_page_count(self.root)

    def exec(self):
        category = Category(
            self.root.find('h1').text,
            self.url + '/index.html',
        )

        books = []

        for i in range(0, self.page_count):
            if i == 0: suffix = '/index.html'
            else: suffix = f'/page-{i+1}.html'

            books.extend(self.exec_page(suffix))

        for book in books:
            category.add_book(book)

        return category

    def exec_page(self, page):
        html = requests.get(self.url + page).content
        root = BeautifulSoup(html, 'html.parser')

        ol = root.find('ol')

        book_links = []

        for li in ol.find_all('li'):
            link = li.find('a')['href']
            link = '/'.join(link.split('/')[-2:])
            link = 'http://books.toscrape.com/catalogue/' + link
            book_links.append(link)

        books = []

        for link in book_links:
            fetcher = BookFetcher(link)
            books.append(fetcher.exec())

        return books

    def get_page_count(self, root):
        page_text = root.find('li', class_='current')
        if page_text is None:
            page_text = 'of 0'
        else:
            page_text = page_text.text
        page_text = page_text[page_text.find('of') + 2:]
        return int(page_text)