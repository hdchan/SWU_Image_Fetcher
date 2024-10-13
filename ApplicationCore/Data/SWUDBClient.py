import json
import urllib.parse
from urllib.request import urlopen

from PyQt5.QtCore import QObject, pyqtSignal

# https://stackoverflow.com/a/33453124
# suggests using move to thread

SWUDB_API_ENDPOINT = 'https://api.swu-db.com/cards/search'

class MockSWUClient(QObject):
    finished = pyqtSignal()
    result_available = pyqtSignal(object)

    def search(self, query):        
            with open('./ApplicationCore/Data/resources/sor.json', 'r') as file:
                json_response = json.load(file)
            self.result_available.emit((json_response, None))
            self.finished.emit()


class SWUDBClient(QObject):
    finished = pyqtSignal()
    result_available = pyqtSignal(object)

    def search(self, query):        
        query = urllib.parse.quote_plus(query)
        url = f'{SWUDB_API_ENDPOINT}?q=name:{query}&format=json'
        try:
            response = urlopen(url)
            json_response = json.load(response)
            self.result_available.emit((json_response, None))
            self.finished.emit()
        except Exception as error:
            self.result_available.emit((None, error))
            self.finished.emit()