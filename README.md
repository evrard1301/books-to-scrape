# Books 2 Scrape

![logo](https://user.oc-static.com/upload/2020/09/22/1600779540759_Online%20bookstore-01.png)


Books to scrape is a learning project proposed by [OpenClassRooms](https://openclassrooms.com/fr/).

This software is a web scraper gathering books data from the website [books.toscrape.com](http://books.toscrape.com/).

By default, it extracts book information within **CSV files** (one by book category) in the ``output/csv`` directory and collects **books images** inside  ``output/img``.

## Quick Start

### Install and run books2scrape

```bash
# create a virtual environment
python3 -m venv env
source env/bin/activate

# clone the project
git clone https://github.com/evrard1301/books-to-scrape.git
cd books-to-scrape

# install dependencies
python3 -m pip install -r requirements.txt

# run books2scrape
python3 books2scrape.py
```

### How to use

books2scrape can be called without any flags.

```shell
python books2scrape.py
```
---

The *.csv* output directory can be specified as the images one using the flags ``--csv-dir`` and ``--img-dir``.

```shell
python books2scrape.py --csv-dir output_csv --img-dir output_img
```

---

books2scrape uses multithreading to speed up the data gathering.
By default, up to 64 threads can be used simultaneously.
This can be changed using the ``-j`` flags.

```shell
# up to eight threads will be used
python books2scrape.py -j 8
```

## License

books2scrape is released under the MIT license.
See the LICENSE.txt file for more information.