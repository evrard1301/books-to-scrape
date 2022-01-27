class Category:
    """
        A named collection of books.
    """
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def __repr__(self):
        return self.name + '\n' + '\n'.join([c.info.title for c in self.books])