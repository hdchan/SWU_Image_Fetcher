from AppCore.Config.Configuration import *

from .APIClientProtocol import APIClientProtocol
from .SWUDB.SWUDBClient import MockSWUDBClient, SWUDBClient


class APIClientProvider:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.mock_client = MockSWUDBClient()
        self.real_client = SWUDBClient()

    def provideClient(self) -> APIClientProtocol:
        if self.configuration.is_mock_data:
            return self.mock_client
        else:
            return self.real_client