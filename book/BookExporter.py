import csv

class BookExporter:
    """
        Export a book in the csv format to a given file.
    """
    def __init__(self, book):
        self.book = book

    def exec(self, file):
        writer = csv.writer(file)

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