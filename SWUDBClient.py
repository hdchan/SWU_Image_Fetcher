import json
import urllib.parse
from urllib.request import urlopen
from PyQt5 import QtCore
import time

# https://stackoverflow.com/a/33453124
# suggests using move to thread

SWUDB_API_ENDPOINT = 'https://api.swu-db.com/cards/search'

class SWUDBClient(QtCore.QObject):

    finished = QtCore.pyqtSignal()
    result_available = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.query = None

    def setQuery(self, query):
        self.query = query

    @QtCore.pyqtSlot()
    def search(self):
        if self.query is None:
            self.finished.emit()
            return
        
        query = urllib.parse.quote_plus(self.query)
        url = f'{SWUDB_API_ENDPOINT}?q=name:{query}&format=json'
        # count = 0
        # while count < 3:
        #     time.sleep(1)
        #     print(f"searching: {query}")
        #     count += 1
        try:
            response = urlopen(url)
            json_response = json.load(response)
            # self.result_available.emit((json_response, None))
            # self.query = None
            # self.finished.emit()
            return (json_response, None)
        except Exception as error:
            return (None, error)
            # self.result_available.emit((None, error))
            # self.query = None
            # self.finished.emit()