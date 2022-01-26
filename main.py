import books_to_scrap
from cli import ArgParser

if __name__ == "__main__":
    args = ArgParser()
    config = args.configuration()

    app = books_to_scrap.App(config)
    app.run('output')
