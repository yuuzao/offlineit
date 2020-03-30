import json
from loguru import logger
from yarl import URL
from pathlib import Path
from typing import List, Dict

from src.adaptor import parser
from src.utils import convert


class Blog:
    __slots__ = ['url', 'headers', 'saver']

    def __init__(self, url: URL, saver: Path):
        self.url = url
        self.saver = Path.home().joinpath(saver)

    def content(self, save=True):
        pr = parser.Parser(self.url)
        contents = pr.parse()
        if save is True:
            self._save(contents)
        else:
            return contents

    def localize(self, raw_html):
        convert(self.url, raw_html)

    def _save(self, contents: List[Dict[str, str]]):
        for post in contents:
            title = post['title']
            file_name = self.saver.joinpath(f'{title}')
            logger.info(f'saving post [{title}] to [{self.saver}]')
            with open(str(file_name), 'w') as f:
                f.write(json.dumps(post))
