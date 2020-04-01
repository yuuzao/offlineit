import json
import time
import httpx
from yarl import URL
from loguru import logger
from pathlib import Path
from typing import List, Dict
from lxml import etree

from src.utils import header


class Converter:
    def __init__(self, url: URL, file_path: Path):
        self.url = URL(url.host)
        self.file_path = file_path
        self.dir_path = file_path.parent
        self.raw_file = self._load_file(file_path)

    def localize_img(self, tag='src'):
        html = etree.fromstring(self.raw_file['article'])
        images = html.xpath('//*/img')

        for e_img in images:
            img_src = URL(e_img.get(tag))
            img_name = img_src.parts[-1]
            file_name = self.dir_path.joinpath(img_name)
            logger.debug(f"file name is [{file_name}]")

            img = self._download_img(img_src)
            with open(str(file_name), 'wb') as f:
                f.write(img)
                logger.info(f'image [{file_name}] downloaded.')

            # convert src urls to local src
            e_img.set(tag, f'./{img_name}')

            time.sleep(1)

        logger.info('write converted html to file')
        self.raw_file['article'] = etree.tostring(html, encoding='unicode')
        with open(str(self.file_path), 'w') as f:
            f.write(json.dumps(self.raw_file))

        logger.info(f"convert ends, downloaded [{len(images)}] images")

    def _download_img(self, url: URL) -> bytes:
        if not url.is_absolute():
            url = self.url.join(url)

        logger.info(f'downloading image from [{url}]')

        remote_img = httpx.get(url.human_repr(), headers=header(url))
        if remote_img.status_code != 200:
            remote_img.raise_for_status()

        return remote_img.content

    @staticmethod
    def _load_file(file_path: Path) -> etree.HTML:
        with open(str(file_path), 'r') as f:
            logger.info(f"loading html from {file_path}")
            raw_html = json.load(f)

        return raw_html
