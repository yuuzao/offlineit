import json
from loguru import logger
from yarl import URL
from pathlib import Path
from typing import List, Dict, Union

from src.adaptor import parser
from src.converter import Converter


class Blog:
    __slots__ = ['url', 'headers', 'saver']

    def __init__(self, url: URL, saver: Path):
        self.url = url
        self.saver = self._extend_saver(base_dir=saver, ex_dir=self.url)
        logger.debug(f'storage directory is [{self.saver}]')

    def content(self) -> List[Path]:
        pr = parser.Parser(self.url)
        contents = pr.parse()

        files = self._save(contents)
        logger.info(f"saved [{len(contents)}] posts, exiting...")

        return files

    def localize(self, entries: List[Path]):
        for entry in entries:
            logger.info(f"localizing [{entry}]...")
            converter = Converter(self.url, entry)
            converter.localize_img()
        logger.info("localize finished")

    def _save(self, contents: List[Dict[str, str]]) -> List[Path]:
        files = []
        for post in contents:
            title = post['title']
            file_name = self._extend_saver(base_dir=self.saver, ex_dir=title).joinpath(f'{title}.json')
            files.append(file_name)

            logger.info(f'saving post [{title}] to [{self.saver}]')

            with open(str(file_name), 'w') as f:
                f.write(json.dumps(post))

        return files

    @staticmethod
    def _extend_saver(base_dir: Path, ex_dir: Union[str, any]) -> Path:
        if isinstance(ex_dir, URL):
            logger.debug('ex_dir is URL')
            ex_dir = ex_dir.host + ex_dir.path
        saver = base_dir.joinpath(ex_dir)
        if not saver.exists():
            saver.mkdir(parents=True, exist_ok=True)

        return saver
