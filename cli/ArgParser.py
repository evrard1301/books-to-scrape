import argparse
import sys

from books_to_scrap import Configuration


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser('books2scrap')
        self.parser.add_argument('--version',
                                 action='store_true',
                                 help='show current version')
        args = self.parser.parse_args(sys.argv[1:])

        if args.version:
            self.version()

    def configuration(self):
        conf = Configuration()
        return conf

    def version(self):
        print('books2scrap v0.0.0')
        exit(0)

    def help(self):
        print('books2scrap usage:')
        print('\t--help, show this help message')
        print('\t--version, show books2scrap version')

