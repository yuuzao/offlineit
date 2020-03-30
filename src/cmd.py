import argparse
from yarl import URL
from typing import Dict


def cmd() -> Dict[str, any]:
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('config')

    args = parser.parse_args()

    return {'url': args.url, 'config': args.ocnfig}
