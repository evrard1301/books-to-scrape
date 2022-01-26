import argparse
import sys

from books_to_scrap import Configuration


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser('books2scrap')
        self.parser.add_argument('--version',
                                 action='store_true',
                                 help='show current version')

        self.parser.add_argument('--csv-dir',
                                 type=str)

        self.parser.add_argument('--img-dir',
                                 type=str)
        self.args = self.parser.parse_args(sys.argv[1:])

        if self.args.version:
            self.version()

    def configuration(self):
        conf = Configuration()

        if self.args.csv_dir is not None:
            conf.csv_output_dir = self.args.csv_dir

        if self.args.img_dir is not None:
            conf.img_output_dir = self.args.img_dir

        return conf

    def version(self):
        print('books2scrap v0.0.0')
        exit(0)

    def help(self):
        print('books2scrap usage:')
        print('\t--help, show this help message')
        print('\t--version, show books2scrap version')

