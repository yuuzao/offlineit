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
        self.dir_path = file_path.parent
        self.html = self._load_file(file_path)

    def localize_img(self, tag='src'):
        images = self.html.xpath('//*/img')
        for e_img in images:
            img_src = e_img.get(tag)
            file_name = self.dir_path.joinpath(img_src.path)

            img = self._download_img(img_src)
            with open(str(file_name), 'wb') as f:
                f.write(img)
                logger.info(f'image [{file_name}] downloaded.')

            e_img.set(tag, f'.{img_src.path}')
            time.sleep(1)

        logger.info(f"downloaded [{len(images)}] images")

    def _download_img(self, url: URL) -> bytes:
        if not url.is_absolute():
            url = self.url.join(url)

        logger.info(f'downloading image from [{url}]')

        remote_img = httpx.get(url, headers=header(url))
        if remote_img.status_code != 200:
            remote_img.raise_for_status()

        return remote_img.content

    @staticmethod
    def _load_file(file_path: Path) -> etree.HTML:
        with open(str(file_path), 'r') as f:
            logger.info(f"loading html from {file_path}")
            raw_html = json.load(f)['article']

        html = etree.HTML(raw_html)
        return html
