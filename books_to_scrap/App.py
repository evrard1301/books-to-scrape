import concurrent
import os
import threading
import requests
from tqdm import tqdm
from book import BookImageDownloader
from books_to_scrap.CategoryCollector import CategoryCollector
from category import CategoryFetcher, CategoryExporter


class App:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.categories = []
        self.max_workers = self.config.jobs

    def run(self):
        output_dir = self.config.csv_output_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.run_categories(output_dir)

        output_dir = self.config.img_output_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.run_images(output_dir)

    def run_categories(self, output_dir):
        collector = CategoryCollector(self.session)
        category_urls = collector.collect()

        categories = []
        self.categories = categories
        progress = tqdm(total=len(category_urls), desc='Load categories')

        def export_category(url, output_dir):
            category = self.fetch_category(url)
            progress.update(1)
            categories.append(category)
            self.export_category(category, output_dir)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for url in category_urls:
                executor.submit(export_category, url, output_dir)
        executor.shutdown(wait=True)
        progress.close()

    def run_images(self, output_dir):
        session = self.session

        progress = tqdm(total=997, desc='Load images')

        def dl_image(the_book):
            dl = BookImageDownloader(the_book, session, output_dir)
            dl.exec()
            progress.update(1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for category in self.categories:
                executor.map(dl_image, category.books)

        executor.shutdown(wait=True)
        progress.close()

    def fetch_category(self, url):
        fetcher = CategoryFetcher(self, url, self.session)
        return fetcher.exec()

    def export_category(self, category, output_dir):
        exporter = CategoryExporter(category)

        with open(os.path.join(os.getcwd(), output_dir, category.name + '.csv'), 'w', encoding='utf-8') as file:
            exporter.exec(file)
