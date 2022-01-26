import os

class BookImageDownloader:
    def __init__(self, book, session, output_dir):
        self.book = book
        self.session = session
        self.output_dir = output_dir

    def exec(self):
        raw = self.session.get(self.book.page.image_url, stream=True).content
        ext = self.book.page.image_url.split('/')[-1].split('.')[1]
        with open(os.path.join(self.output_dir,
                               self.book.info.title.replace('/', '_') + '.' + ext),
                  'wb') as file:
            file.write(raw)
