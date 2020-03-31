import json
from loguru import logger
from yarl import URL
from pathlib import Path
from typing import List, Dict, Union

from src.adaptor import parser
from src.utils import convert


class Blog:
    __slots__ = ['url', 'headers', 'saver']

    def __init__(self, url: URL, saver: Path):
        self.url = url
        self.saver = self._extend_saver(base_dir=saver, ex_dir=self.url)
        logger.debug(f'storage directory is [{self.saver}]')

    def content(self, save=True):
        pr = parser.Parser(self.url)
        contents = pr.parse()

        if save is True:
            self._save(contents)
            logger.info(f"saved [{len(contents)}] posts, exiting...")

        return contents

    def localize(self, raw_html):
        convert(self.url, raw_html)

    def _save(self, contents: List[Dict[str, str]]):
        for post in contents:
            title = post['title']
            file_name = self._extend_saver(base_dir=self.saver, ex_dir=title).joinpath(f'{title}.json')
            logger.info(f'saving post [{title}] to [{self.saver}]')

            with open(str(file_name), 'w') as f:
                f.write(json.dumps(post))

    @staticmethod
    def _extend_saver(base_dir: Path, ex_dir: Union[str, any]) -> Path:
        if isinstance(ex_dir, URL):
            logger.debug('ex_dir is URL')
            ex_dir = ex_dir.host + ex_dir.path
        saver = base_dir.joinpath(ex_dir)
        if not saver.exists():
            saver.mkdir(parents=True, exist_ok=True)

        return saver
