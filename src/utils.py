from pathlib import Path
from yarl import URL
from typing import Dict
from loguru import logger
from lxml import etree


def header(url: URL, extra: Dict = None) -> Dict:
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Host": url.host,
        "Connection": "keep-alive",
        "Referer": "www.google.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    }

    if extra is not None:
        headers.update(extra)

    return headers


def convert(host: URL, raw_html: str):
    """
    convert image links to local resources.
    """
    html = etree.fromstring(raw_html)
    # note: some links may be relative.


def verify_dir(dir_path: Path):
    if not dir_path.exists():
        logger.info(f'creating directory at [{dir_path}] with permission [777]')
        dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path
