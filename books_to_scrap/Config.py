class Configuration:
    """
        Holds the configuration of books2scrape.
    """

    def __init__(self):
        self.version = '0.0.0'
        self.jobs = 64
        self.csv_output_dir = 'output/csv'
        self.img_output_dir = 'output/img'
        self.failure_attempts = 8
