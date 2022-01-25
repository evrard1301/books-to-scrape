import concurrent
import os
import threading
import requests

from book import BookImageDownloader
from books_to_scrap.CategoryCollector import CategoryCollector
from category import CategoryFetcher, CategoryExporter


class App:
    def __init__(self):
        self.session = requests.Session()
        self.categories = []
        self.max_workers = 256

    def run(self, output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        self.run_categories(output_dir)
        self.run_images(output_dir)

    def run_categories(self, output_dir):
        collector = CategoryCollector(self.session)
        category_urls = collector.collect()

        categories = []
        self.categories = categories

        def export_category(url, output_dir):
            category = self.fetch_category(url)
            categories.append(category)
            self.export_category(category, output_dir)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for url in category_urls:
                executor.submit(export_category, url, output_dir)
        executor.shutdown(wait=True)

    def run_images(self, output_dir):
        session = self.session
        mutex = threading.Lock()

        def dl_image(the_book):
            dl = BookImageDownloader(the_book, session, output_dir)
            dl.exec()

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for category in self.categories:
                executor.map(dl_image, category.books)
                #for book in category.books:
                #    executor.submit(dl_image, book)
        executor.shutdown(wait=True)

    def fetch_category(self, url):
        fetcher = CategoryFetcher(url, self.session)
        return fetcher.exec()


    def export_category(self, category, output_dir):
        exporter = CategoryExporter(category)

        with open(os.path.join(os.getcwd(), output_dir, category.name + '.csv'), 'w') as file:
            exporter.exec(file)
