from ..Config.Configuration import *
from .ImageFetcher import MockImageFetcher, RemoteImageFetcher
from .ImageFetcherProtocol import *


class ImageFetcherProvider:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.real_client = RemoteImageFetcher()
        self.mock_client = MockImageFetcher()

    def provideImageFetcher(self) -> ImageFetcherProtocol:
        if self.configuration.is_mock_data:
            return self.mock_client
        else:
            return self.real_client
