import os
import threading
import requests

from books_to_scrap.CategoryCollector import CategoryCollector
from category import CategoryFetcher, CategoryExporter


class App:
    def __init__(self):
        self.session = requests.Session()

    def run(self, output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        self.run_single(output_dir)

    def run_single(self, output_dir):
        collector = CategoryCollector(self.session)
        category_urls = collector.collect()

        counter = 0

        def export_category(url, output_dir):
            category = self.fetch_category(url)
            self.export_category(category, output_dir)

        threads = []

        for url in category_urls:
            t = threading.Thread(target=export_category, args=(url, output_dir))
            threads.append(t)
            t.start()
            counter += 1

        for t in threads:
            t.join()

        print('done')

    def fetch_category(self, url):
        fetcher = CategoryFetcher(url, self.session)
        return fetcher.exec()

    def export_category(self, category, output_dir):
        exporter = CategoryExporter(category)

        with open(os.path.join(os.getcwd(), output_dir, category.name + '.csv'), 'w') as file:
            exporter.exec(file)
