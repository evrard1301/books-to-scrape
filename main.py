from book import BookFetcher

if __name__ == '__main__':
    print('Books 2 Scrape')
    fetcher = BookFetcher('http://books.toscrape.com/catalogue/shakespeares-sonnets_989/index.html')
    book = fetcher.exec()

    print(book)