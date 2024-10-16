from typing import Callable, List, Tuple

from ..Network import Networker
from ..Models.TradingCard import *

APIClientSearchCallback = Callable[[Tuple[List[TradingCard], Optional[Exception]]], None]

class APIClientProtocol:
    def __init__(self, networker: Networker):
        self.netorker = networker
        
    def search(self, query: str, callback: APIClientSearchCallback) -> None:
        raise Exception()