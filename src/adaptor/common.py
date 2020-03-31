from yarl import URL
import httpx
import time
from typing import List, Dict, Union
from loguru import logger

from src.utils import header


class Common:
    def __init__(self, url: URL):
        self.url = url
        self.headers = header(url)
        self.client = httpx.Client()

    def __call__(self, *args, **kwargs) -> List[Dict[str, str]]:
        articles = self.run()
        self.client.close()
        logger.info(f"blog parse finished, obtained {len(articles)} in total")

        return articles

    def run(self) -> List[Dict[str, str]]:
        total_pages = self.max_pages(self.client)

        pages = self.assemble_page_url(total_pages)
        post_urls = [self.fetch_post_urls(p) for p in pages][0]

        logger.info(f'obtained {len(post_urls)} post urls in total')

        articles: List[Dict[str, str]] = []
        url: URL
        for url in post_urls:
            articles.append(self.parse_article(url))
            time.sleep(1)

        return articles

    def max_pages(self, client: httpx.Client() = None) -> int:
        return 0

    def fetch_post_urls(self, page: URL, client: httpx.Client() = None) -> List[URL]:
        return []

    def parse_article(self, post_url: URL, client: httpx.Client = None) -> Union[Dict[str, str], any]:
        return []

    @staticmethod
    def _req(client: httpx.Client, url: URL, headers: Dict):
        logger.debug(f'request url is {url}')
        res = client.get(url.human_repr(), headers=headers)
        if res.status_code != 200:
            res.raise_for_status()

        return res

    @staticmethod
    def assemble_page_url(max_page: int) -> List[URL]:
        return []
