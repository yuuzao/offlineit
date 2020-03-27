import argparse
from yarl import URL


def cmd() -> URL:
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    url = parser.parse_args().url
    return URL(url)
