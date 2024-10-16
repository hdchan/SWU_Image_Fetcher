import json
import urllib.parse
from typing import Any, Dict, List

from ...Data.APIClientProtocol import (APIClientProtocol,
                                       APIClientSearchCallback)
from ...Models.TradingCard import TradingCard
from ...Network import NetworkRequestResponse
from urllib.request import Request

# https://stackoverflow.com/a/33453124
# suggests using move to thread

class SWUTradingCard(TradingCard):
    @classmethod
    def from_swudb_response(cls, json: Dict[str, Any]):
        obj = cls.__new__(cls)
        super(SWUTradingCard, obj).__init__(
            name=json['Name'],
            set=json['Set'],
            type=json['Type'],
            front_art=json['FrontArt'],
            number=json['Number'],
            back_art=json.get('BackArt', None)
        )
        return obj

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
        
        
class MockSWUDBClient(APIClientProtocol):
    
    # TODO: need to hook up developer delay here
    def search(self, query: str, callback: APIClientSearchCallback):
        with open('./AppCore/Data/SWUDB/sor.json', 'r') as file:
            json_response = json.load(file)
        result_list: List[TradingCard] = []
        for i in json_response['data']:
                swu_card = SWUTradingCard.from_swudb_response(i)
                result_list.append(swu_card)
        callback((result_list, None))