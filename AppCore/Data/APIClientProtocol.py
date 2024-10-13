from typing import Any, Callable, List, NewType, Tuple

from ..Models.TradingCard import *


# APIClientSearchCallback = NewType("APIClientSearchCallback", Callable[[List[TradingCard], None], None])
class APIClientProtocol:
    def search(self, query: str, callback):
        raise Exception()