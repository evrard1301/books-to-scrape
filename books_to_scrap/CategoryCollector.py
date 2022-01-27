from bs4 import BeautifulSoup


class CategoryCollector:
    """
        Collect all the URLs of each book categories.
    """
    def __init__(self, session):
        self.session = session
        self.url = 'http://books.toscrape.com/index.html'

    def collect(self):
        root = BeautifulSoup(self.session.get(self.url).content, 'html.parser')
        tmp = root.find('div', class_='side_categories')
        assert(tmp is not None)
        all_category_li = tmp.find('ul').find_all('li')

        urls = []

        for category_li in all_category_li:
            url = 'http://books.toscrape.com/' + category_li.find('a')['href']
            urls.append(url)

        return urls[1:]
