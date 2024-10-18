  
import json
import time
from typing import List
from urllib.request import Request, urlopen

from PyQt5.QtCore import QObject, pyqtSignal

from ...Data.APIClientProtocol import (APIClientProtocol,
                                       APIClientSearchCallback)
from ...Models.TradingCard import TradingCard
from .SWUTradingCard import SWUTradingCard


class MockSWUDBClient(APIClientProtocol):
    class ClientWorker(QObject):
        finished = pyqtSignal()
        result_available = pyqtSignal(object)

        def __init__(self, delay: int):
            super().__init__()
            self.delay = delay

        def load(self, request: Request):
            try:
                time.sleep(self.delay) # for debugging
                response = urlopen(request)
                json_response = json.load(response)
                self.result_available.emit((json_response, None))
                self.finished.emit()
            except Exception as error:
                self.result_available.emit((None, error))
                self.finished.emit()
    
    # TODO: need to hook up developer delay here
    def search(self, query: str, callback: APIClientSearchCallback):
        with open('./AppCore/Clients/SWUDB/sor.json', 'r') as file:
            json_response = json.load(file)
        result_list: List[TradingCard] = []
        for i in json_response['data']:
                swu_card = SWUTradingCard.from_swudb_response(i)
                result_list.append(swu_card)
        callback((result_list, None))