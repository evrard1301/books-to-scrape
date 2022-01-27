import csv
from book import BookExporter


class CategoryExporter:
    """
        Write a csv formatted file containing one entry per book.
    """
    def __init__(self, category):
        self.category = category

    def exec(self, file):
        writer = csv.writer(file)

        writer.writerow([
                'product_page_url',
                'universal_ product_code (upc)',
                'title',
                'price_including_tax',
                'price_excluding_tax',
                'number_available',
                'product_description',
                'category',
                'review_rating',
                'image_url'
            ])

        for book in self.category.books:
            exporter = BookExporter(book)
            exporter.exec(file)
