class BookInfo:
    def __init__(self, upc, title, desc, cat):
        self.universal_product_code = upc
        self.title = title
        self.description = desc
        self.category = cat


class BookPrice:
    def __init__(self, tax, no_tax):
        self.tax_price = tax
        self.no_tax_price = no_tax


class BookPage:
    def __init__(self, url, img_url, nb_available, review):
        self.url = url
        self.image_url = img_url
        self.number_available = nb_available
        self.review_rating = review


class Book:
    def __init__(self, info, page, price):
        self.info = info
        self.page = page
        self.price = price

    def __repr__(self):
        return '\n'.join([
            f'page: {self.page.url}',
            f'universal product code: {self.info.universal_product_code}',
            f'title: {self.info.title}',
            f'price (tax): {self.price.tax_price}',
            f'price (no tax): {self.price.no_tax_price}',
            f'number available: {self.page.number_available}',
            f'product description: {self.info.description}',
            f'category: {self.info.category}',
            f'review rating: {self.page.review_rating}',
            f'image url: {self.page.image_url}'

        ])
