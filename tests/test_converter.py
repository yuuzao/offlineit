import pytest
from pathlib import Path
from yarl import URL
from lxml import etree

from src.converter import Converter


def test_converter():
    file = Path.cwd().joinpath('mocks/test_converter.json')
    file_dir = Path.cwd().joinpath('mocks')
    base_url = URL("https://www.cnblog.com")

    converter = Converter(base_url, file)
    converter.localize_img()

    handled = etree.fromstring(converter._load_file(file)['article'])
    handled_img = handled.xpath('//*/img')[0].get('src')

    test_img = Path('./1004427-20200329151921980-987119585.png')
    relative_url = f'./{test_img}'

    assert file_dir.joinpath(test_img).exists() is True
    assert handled_img == relative_url
