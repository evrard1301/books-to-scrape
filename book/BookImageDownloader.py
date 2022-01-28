import os
import time
import colorama


class BookImageDownloader:
    """
        Download the main image of a given book
        inside a given output directory.
    """

    def __init__(self, book, config, session, output_dir):
        self.book = book
        self.config = config
        self.session = session
        self.output_dir = output_dir

    def exec(self):
        nb_attempts = self.config.failure_attempts
        done = False
        for i in range(0, nb_attempts):
            try:
                raw = self.session.get(
                    self.book.page.image_url, stream=True).content
                ext = self.book.page.image_url.split('/')[-1].split('.')[1]
                with open(os.path.join(self.output_dir,
                                       self.book.info.universal_product_code
                                       + '_' + self.book.info
                                                .title
                                                .replace('/', '_') + '.'
                                                                   + ext),
                          'wb') as file:
                    file.write(raw)
                done = True
                break
            except Exception:
                print(colorama.Fore.LIGHTRED_EX
                      + f'E: download failed for {self.book.info.title} image')
                print(colorama.Fore.YELLOW
                      + f'W: retrying {i+1}/{nb_attempts}')
                time.sleep(1.0)
        if done is False:
            print(colorama.Fore.WHITE + colorama.Back.RED
                  + f'E: failure downloading {self.book.info.title} image',
                  flush=True,
                  end='')
            print()
        print(colorama.Style.RESET_ALL, end='', flush=True)
