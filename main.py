from book import BookFetcher, BookExporter
from category import CategoryFetcher


def main():
    print('Books 2 Scrape')

    fetcher = CategoryFetcher('http://books.toscrape.com/catalogue/category/books/mystery_3/index.html')
    category = fetcher.exec()

    print(category)


if __name__ == "__main__":
    main()
