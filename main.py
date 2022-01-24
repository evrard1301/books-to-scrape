from book import BookFetcher, BookExporter
from category import CategoryFetcher, CategoryExporter


def main():
    print('Books 2 Scrape')

    fetcher = CategoryFetcher('http://books.toscrape.com/catalogue/category/books/mystery_3/index.html')
    category = fetcher.exec()

    exporter = CategoryExporter(category)

    with open(f'{category.name}.csv', 'w') as file:
        exporter.exec(file)

if __name__ == "__main__":
    main()
