from bs4 import BeautifulSoup
from book import BookFetcher
from category import Category
import concurrent.futures
import time
import colorama


class CategoryFetcher:
    """
        Create a category object containing book objects.
    """

    def __init__(self, app, url, session):
        self.app = app
        self.session = session
        self.url = '/'.join(url.split('/')[:-1])
        self.root = BeautifulSoup(
            self.session.get(self.url + '/' + 'index.html')
                .content, 'html.parser')

        self.page_count = self.get_page_count(self.root)

        self.max_workers = self.app.config.jobs

    def exec(self):
        category = Category(
            self.root.find('h1').text,
            self.url + '/index.html',
        )

        return self.exec_pages(category)

    def exec_pages(self, category):

        with concurrent\
                .futures\
                .ThreadPoolExecutor(max_workers=self.max_workers)\
                as executor:
            for i in range(0, self.page_count):
                if i == 0:
                    suffix = '/index.html'
                else:
                    suffix = f'/page-{i + 1}.html'

                executor.submit(self.exec_page, suffix, category)
        executor.shutdown(wait=True)
        return category

    def exec_page(self, page, category):
        html = self.session.get(self.url + page).content
        root = BeautifulSoup(html, 'html.parser')

        ol = root.find('ol')

        book_links = []

        for li in ol.find_all('li'):
            link = li.find('a')['href']
            link = '/'.join(link.split('/')[-2:])
            link = 'http://books.toscrape.com/catalogue/' + link
            book_links.append(link)

        books = []

        def get_book(my_link):
            for i in range(0, self.app.config.failure_attempts):
                try:
                    fetcher = BookFetcher(my_link, self.session)
                    books.append(fetcher.exec())
                    break
                except Exception as err:
                    print('error fetching book', err)
                    print(colorama.Fore.YELLOW,
                          f'retrying {i+1}/{self.app.config.failure_attempts}')
                    print(colorama.Style.RESET_ALL, end='', flush=True)
                    time.sleep(1)

        with concurrent\
                .futures\
                .ThreadPoolExecutor(max_workers=self.max_workers)\
                as executor:
            for link in book_links:
                executor.submit(get_book, link)

        executor.shutdown(wait=True)

        for book in books:
            category.add_book(book)

    @staticmethod
    def get_page_count(root):
        page_text = root.find('li', class_='current')
        if page_text is None:
            page_text = 'of 0'
        else:
            page_text = page_text.text
        page_text = page_text[page_text.find('of') + 2:]
        res = int(page_text)
        if res == 0:
            res += 1
        return res
