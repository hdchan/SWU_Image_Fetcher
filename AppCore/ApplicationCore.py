from typing import List

from .Data import APIClientProvider, DataSource
from .Image import ImageFetcherProvider, ImageResourceManager
from .Models.TradingCard import TradingCard
from .Observation import ObservationTower
from .Observation.Events import *


class ApplicationCore:

    def __init__(self, observation_tower: ObservationTower, 
                 api_client_provider: APIClientProvider,
                 image_fetcher_provider: ImageFetcherProvider):
        self._data_source = DataSource(api_client_provider)
        self._data_source.delegate = self
        self._resource_manager = ImageResourceManager(image_fetcher_provider)
        self._resource_manager.delegate = self
        
        self._observation_tower = observation_tower
        self.current_card_search_resource = None
        self.can_publish = False
        self.delegate = None

    @property
    def resource_manager(self) -> ImageResourceManager:
        return self._resource_manager

    # MARK: - Datasource
    def search(self, query: str):
        self._observation_tower.notify(SearchEvent(SearchEvent.EventType.STARTED))
        self._data_source.search(query)

    def select_card_resource_for_card_selection(self, index: int):
        self._data_source.select_card_resource_for_card_selection(index)

    def flip_current_previewed_card(self):
        # TODO: flipped card saved both sides as front some how
        self._data_source.flip_current_previewed_card()

    def current_previewed_trading_card_is_flippable(self) -> bool:
        return self._data_source.current_previewed_trading_card_is_flippable()

    # MARK: - DS Delegate methods
    def ds_completed_search_with_result(self, ds: DataSource, result_list: List[TradingCard], error: Exception):
        display_name_list = list(map(lambda x: x.friendly_display_name, result_list))
        self.delegate.app_did_complete_search(self, display_name_list, error)
        self._observation_tower.notify(SearchEvent(SearchEvent.EventType.FINISHED))

    def ds_did_retrieve_card_resource_for_card_selection(self, ds: DataSource, trading_card: TradingCard, is_flippable: bool):
        local_card_resource = self._resource_manager.generate_local_card_resource(trading_card)
        self._resource_manager.async_store_local_resource(trading_card, local_card_resource)
        self.delegate.app_did_retrieve_card_resource_for_card_selection(self, local_card_resource, is_flippable)
        self.current_card_search_resource = local_card_resource
    
    # MARK: - Resource manager
    def can_stage_current_card_search_resource_to_stage_index(self, index: int) -> bool:
        return self.current_card_search_resource is not None and index < len(self._resource_manager.production_resources)

    def stage_resource(self, index: int):
        self._resource_manager.stage_resource(self.current_card_search_resource, index)
        self._retrieve_publish_status_and_notify_if_needed()

    def unstage_resource(self, index: int):
        self._resource_manager.unstage_resource(index)
        self._retrieve_publish_status_and_notify_if_needed()

    def unstage_all_resources(self):
        self._resource_manager.unstage_all_resources()
        self._retrieve_publish_status_and_notify_if_needed()

    def load_production_resources(self):
        self._resource_manager.load_production_resources()


    def can_publish_staged_resources(self) -> bool:
        return self._resource_manager.can_publish_staged_resources()

    def publish_staged_resources(self) -> bool:
        return self._resource_manager.publish_staged_resources()


    # MARK: - RM Delegate methods
    def rm_did_load_production_resources(self, rm: ImageResourceManager, production_resources: List[LocalCardResource]):
        self.delegate.app_did_load_production_resources(self, production_resources)

    def rm_did_finish_storing_local_resource(self, rm: ImageResourceManager, local_resource: LocalCardResource):
        self._observation_tower.notify(LocalResourceReadyEvent(local_resource))
        self._retrieve_publish_status_and_notify_if_needed()

    
    def _retrieve_publish_status_and_notify_if_needed(self):
        publish_status = self._resource_manager.can_publish_staged_resources()
        # Needs mutex if we're keeping state here
        # if self.can_publish != publish_status:
        self.can_publish = publish_status
        self.delegate.app_publish_status_changed(publish_status)

        