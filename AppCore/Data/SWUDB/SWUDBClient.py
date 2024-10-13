import json
import urllib.parse
from functools import partial
from urllib.request import urlopen

from PyQt5.QtCore import QObject, QThread, pyqtSignal

from ...Models.TradingCard import TradingCard
from ..APIClientProtocol import APIClientProtocol
from typing import List, Callable
# https://stackoverflow.com/a/33453124
# suggests using move to thread

class SWUTradingCard(TradingCard):
    @classmethod
    def from_swudb_response(cls, json):
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

class MockSWUDBClient(APIClientProtocol):
    def search(self, query: str, callback):
        with open('./AppCore/Data/SWUDB/sor.json', 'r') as file:
            json_response = json.load(file)
        result_list: List[TradingCard] = []
        for i in json_response['data']:
                swu_card = SWUTradingCard.from_swudb_response(i)
                result_list.append(swu_card)
        callback((result_list, None))


class SWUDBClient(APIClientProtocol):
    class ClientWorker(QObject):
        finished = pyqtSignal()
        result_available = pyqtSignal(object)

        def search(self, url: str):
            try:
                response = urlopen(url)
                json_response = json.load(response)
                self.result_available.emit((json_response, None))
                self.finished.emit()
            except Exception as error:
                self.result_available.emit((None, error))
                self.finished.emit()

    SWUDB_API_ENDPOINT = 'https://api.swu-db.com/cards/search'

    def search(self, query: str, callback):
        def completed_search(result):
            json_response, error = result
            result_list = []
            if json_response is not None:
                for i in json_response['data']:
                    swu_card = SWUTradingCard.from_swudb_response(i)
                    result_list.append(swu_card)
            callback((result_list, error))
      
        query = urllib.parse.quote_plus(query)
        url = f'{self.SWUDB_API_ENDPOINT}?q=name:{query}&format=json'
        thread = QThread()
        worker = SWUDBClient.ClientWorker()
        worker.moveToThread(thread)
        thread.started.connect(partial(worker.search, url))
        worker.result_available.connect(completed_search)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        self.latest_thread = thread
        thread.start()

    