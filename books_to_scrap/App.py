import concurrent.futures
import os
import time
import requests
from tqdm import tqdm
from book import BookImageDownloader
from books_to_scrap.CategoryCollector import CategoryCollector
from category import CategoryFetcher, CategoryExporter


class App:
    """
        Launch the gathering of all books by categories and theirs images.
        App uses a configuration object to set up
        threads and output directories.
    """

    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.categories = []
        self.max_workers = self.config.jobs
        self.books_count = 0

    def run(self):
        output_dir = self.config.csv_output_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.run_categories(output_dir)

        output_dir = self.config.img_output_dir

        self.run_images(output_dir)

    def run_categories(self, output_dir):
        collector = CategoryCollector(self.session)
        category_urls = collector.collect()

        categories = []
        self.categories = categories
        progress = tqdm(total=len(category_urls), desc='Load categories')

        def export_category(my_url, my_output_dir):
            for i in range(0, self.config.failure_attempts):
                try:
                    category = self.fetch_category(my_url)
                    progress.update(1)
                    categories.append(category)
                    self.export_category(category, my_output_dir)
                    self.books_count += len(category.books)
                    break
                except Exception:
                    print(
                        f'error exporting category, retry {i + 1}/'
                        + '{self.config.failure_attempts}')
                    time.sleep(1)

        with concurrent\
                .futures\
                .ThreadPoolExecutor(max_workers=self.max_workers) \
                as executor:
            for url in category_urls:
                executor.submit(export_category, url, output_dir)
        executor.shutdown(wait=True)
        progress.close()

    def run_images(self, output_dir):
        session = self.session

        progress = tqdm(total=self.books_count, desc='Load images')

        def dl_image(the_book):
            try:
                dir_name = the_book.info.category.replace('/', '_')
                category_dir = os.path.join(output_dir, dir_name)
                if not os.path.exists(category_dir):
                    try:
                        os.makedirs(category_dir)
                    except OSError:
                        pass

                dl = BookImageDownloader(
                    the_book, self.config, session, category_dir)
                dl.exec()

                progress.update(1)
            except Exception as err:
                print(f'Error loading {the_book.info.title} image\n\n{err}')

        with concurrent\
                .futures\
                .ThreadPoolExecutor(max_workers=self.max_workers) \
                as executor:

            for category in self.categories:
                try:
                    executor.map(dl_image, category.books)
                except Exception as err:
                    print('error fetching image\n\n', err)

        executor.shutdown(wait=True)
        progress.close()

    def fetch_category(self, url):
        fetcher = CategoryFetcher(self, url, self.session)
        return fetcher.exec()

    @staticmethod
    def export_category(category, output_dir):
        exporter = CategoryExporter(category)

        with open(os.path.join(os.getcwd(),
                               output_dir,
                               category.name + '.csv'),
                  'w',
                  encoding='utf-8') as file:
            exporter.exec(file)
