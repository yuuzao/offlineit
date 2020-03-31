from typing import List, Dict
from yarl import URL

from src.adaptor.common import Common
import httpx
from dateutil.parser import parse as parse_date
from loguru import logger
from lxml import etree


class Cnblogs(Common):
    def __init__(self, url):
        super(Cnblogs, self).__init__(url)
        self.url = self.adjust_url()
        logger.debug(f'self.url is changed to {self.url}')

    def max_pages(self, client: httpx.Client() = None) -> int:
        page_url = self.url.build(scheme='https', host=self.url.host, path=f'{self.url.path}/default.html')

        cli = client if client is not None else self.client
        # in order to detect the max page number, it has to begin at page 2.
        p_url = page_url.with_query('page=2')
        page = self._req(cli, p_url, self.headers)

        html = etree.HTML(page.text)
        pager = html.xpath('//*[@id="homepage_top_pager"]//a')

        if len(pager) == 0:
            return 1
        elif len(pager) == 2:
            return 2
        else:
            i = int(pager[-2].text)
            logger.info(f'detected total pages of {i}')
            return i

    def fetch_post_urls(self, page: URL, client: httpx.Client() = None) -> List[URL]:
        logger.info('start to parse post urls')
        cli = client if client is not None else self.client
        page = self._req(cli, page, self.headers)

        html = etree.HTML(page.text)
        posts = html.xpath('//*[@id="mainContent"]//*[@class="day"]//a[@class="postTitle2"]')
        post_urls = [URL(p.attrib['href']) for p in posts]
        logger.info(f'obtained {len(post_urls)} post urls')

        return post_urls

    def parse_article(self, post_url: URL, client: httpx.Client = None) -> Dict[str, str]:
        logger.info(f'start to fetch articles from {post_url}')
        cli = client if client is not None else self.client
        page = self._req(cli, post_url, self.headers)

        html = etree.HTML(page.text)
        post_title = html.xpath('//*[@id="cb_post_title_url"]')[0].text

        raw_content = html.xpath('//*[@id="cnblogs_post_body"]')[0]
        post_content = etree.tostring(raw_content, encoding='unicode')

        post_date = html.xpath('//*[@id="post-date"]')[0].text

        article = {"title": post_title, "article": post_content, "date": post_date}
        logger.info(f'article parsed: [{post_title}]')
        return article

    def assemble_page_url(self, max_page: int) -> List[URL]:
        pages = [self.url.with_query(f'page={i}') for i in range(1, max_page + 1)]

        return pages

    def adjust_url(self) -> URL:
        logger.info("adjusting blog's url")
        scheme = 'https'
        host = self.url.host

        # the first part of the url's path, which represents the blog's id
        path = self.url.parts[1]

        new_url = self.url.build(scheme=scheme, host=host).with_path(path)
        logger.debug(f"blog's url is {new_url}")
        return new_url
