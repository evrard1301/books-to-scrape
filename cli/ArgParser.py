import argparse
import sys

from books_to_scrap import Configuration


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser('books2scrap')
        self.parser.add_argument('--version', '-v',
                                 action='store_true',
                                 help='show current version')

        self.parser.add_argument('--csv-dir',
                                 type=str,
                                 help='set the csv files output directory')

        self.parser.add_argument('--img-dir',
                                 type=str,
                                 help='set the image files output directory')

        self.parser.add_argument('--jobs', '-j',
                                 type=int,
                                 help='set the jobs number')

        self.parser.add_argument('--tentatives', '-t',
                                 type=int,
                                 help='set the maximum of downloading attempts'
                                 + ' after a failure'
                                 )

        self.args = self.parser.parse_args(sys.argv[1:])

        if self.args.version:
            self.version()

    def configuration(self):
        conf = Configuration()

        if self.args.csv_dir is not None:
            conf.csv_output_dir = self.args.csv_dir

        if self.args.img_dir is not None:
            conf.img_output_dir = self.args.img_dir

        if self.args.jobs is not None:
            conf.jobs = self.args.jobs

        if self.args.tentatives is not None:
            conf.failure_attempts = self.args.tentatives

        return conf

    @staticmethod
    def version():
        print('books2scrap v0.0.0')
        exit(0)

    @staticmethod
    def help():
        print('books2scrap usage:')
        print('\t--help, show this help message')
        print('\t--version, show books2scrap version')
