import csv

class BookExporter:
    def __init__(self, book):
        self.book = book

    def exec(self, output_file):
        with open(output_file, 'w') as file:
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

            writer.writerow([
                self.book.page.url,
                self.book.info.universal_product_code,
                self.book.info.title,
                self.book.price.tax_price,
                self.book.price.no_tax_price,
                self.book.page.number_available,
                self.book.info.description,
                self.book.info.category,
                self.book.page.review_rating,
                self.book.page.image_url
            ])