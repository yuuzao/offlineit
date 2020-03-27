from yarl import URL

from src.adaptor import parser


class Blog:
    __slots__ = ['url', 'headers']

    def __init__(self, url: URL):
        self.url = url

    def content(self):
        pr = parser.Parser(self.url)
        return pr.parse()
