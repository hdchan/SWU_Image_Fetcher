import urllib.parse
from typing import Any, Dict, List
from urllib.request import Request

from ...Data.APIClientProtocol import (APIClientProtocol,
                                       APIClientSearchCallback)
from ...Models.TradingCard import TradingCard
from ...Network import NetworkRequestResponse
from .SWUTradingCard import SWUTradingCard

# https://stackoverflow.com/a/33453124
# suggests using move to thread



class SWUDBClient(APIClientProtocol):

    def search(self, query: str, callback: APIClientSearchCallback):
        class SearchRequestResponse(NetworkRequestResponse[List[TradingCard]]):
            SWUDB_API_ENDPOINT = 'https://api.swu-db.com/cards/search'
            
            def __init__(self, query: str):
                self.query = query
            
            def request(self) -> Request:
                query = urllib.parse.quote_plus(self.query)
                url = f'{self.SWUDB_API_ENDPOINT}?q=name:{query}&format=json'
                return Request(url)
            def decode(self, json: Dict[str, Any]) -> List[TradingCard]:
                result_list: List[TradingCard] = []
                for i in json['data']:
                    swu_card = SWUTradingCard.from_swudb_response(i)
                    result_list.append(swu_card)
                return result_list
            
        self.netorker.load(SearchRequestResponse(query), callback)
        
      