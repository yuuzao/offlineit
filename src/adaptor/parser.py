from yarl import URL
from typing import Callable, List, Dict

from src.adaptor.cnblogs import Cnblogs
from src.adaptor.common import Common


class Parser:

    def __init__(self, url: URL):
        self.url = url

    def parse(self) -> List[Dict[str, str]]:
        parser = self._select_adaptor()
        articles = parser(self.url)()

        return articles

    def _select_adaptor(self) -> Callable:

        if 'cnblogs' in self.url.human_repr():
            parser = Cnblogs
        else:
            parser = Common

        return parser
