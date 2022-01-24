from book import BookFetcher, BookExporter

if __name__ == '__main__':
    print('Books 2 Scrape')

    fetcher = BookFetcher('http://books.toscrape.com/catalogue/the-selfish-gene_81/index.html')
    book = fetcher.exec()

    exporter = BookExporter(book)
    exporter.exec(book.info.title + '.csv')
