from typing import List, Optional

from .Data import APIClientProvider, CardDataSource
from .Image import (ImageFetcherProvider, ImageResourceCacher)
from .Models.TradingCard import TradingCard
from .Observation import ObservationTower
from .Observation.Events import *


class CardSearchFlow:
    def __init__(self, 
                 observation_tower: ObservationTower, 
                 api_client_provider: APIClientProvider,
                 image_fetcher_provider: ImageFetcherProvider, 
                 configuration: Configuration):
        self._data_source = CardDataSource(api_client_provider)
        self._data_source.delegate = self
        self._resource_cacher = ImageResourceCacher(image_fetcher_provider, 
                                                    configuration)
        self._resource_cacher.delegate = self
        
        self._observation_tower = observation_tower
        self.current_card_search_resource: Optional[LocalCardResource] = None
        self.delegate = None

    # MARK: - Datasource
    def search(self, query: str):
        self._data_source.search(query)

    def select_card_resource_for_card_selection(self, index: int):
        self._data_source.select_card_resource_for_card_selection(index)

    def flip_current_previewed_card(self):
        self._data_source.flip_current_previewed_card()

    def current_previewed_trading_card_is_flippable(self) -> bool:
        return self._data_source.current_previewed_trading_card_is_flippable()

    # MARK: - DS Delegate methods
    def ds_completed_search_with_result(self, ds: CardDataSource, result_list: List[TradingCard], error: Exception):
        self._resource_cacher.attach_local_resources(result_list)
        self.delegate.sf_did_complete_search(self, result_list, error)

    def ds_did_retrieve_card_resource_for_card_selection(self, ds: CardDataSource, trading_card: TradingCard, is_flippable: bool):
        self._resource_cacher.async_store_local_resource(trading_card)
        self.delegate.sf_did_retrieve_card_resource_for_card_selection(self, trading_card)
        self.current_card_search_resource = trading_card.local_resource

    # MARK: - Resource Cacher Delegate
    def rc_did_finish_storing_local_resource(self, rm: ImageResourceCacher, local_resource: LocalCardResource):
        self._observation_tower.notify(LocalResourceReadyEvent(local_resource))
        self.delegate.sf_did_finish_storing_local_resource(self, local_resource)