from typing import List

from .Data import APIClientProvider
from .Image import (ImageFetcherProvider,
                    ImageResourceDeployer)
from .Models.TradingCard import TradingCard
from .Observation import ObservationTower
from .Observation.Events import *
from .CardSearchFlow import CardSearchFlow

class ApplicationCore:
    def __init__(self, 
                 observation_tower: ObservationTower, 
                 api_client_provider: APIClientProvider,
                 image_fetcher_provider: ImageFetcherProvider, 
                 configuration: Configuration):
        self._card_search_flow = CardSearchFlow(observation_tower, 
                                                api_client_provider, 
                                                image_fetcher_provider, 
                                                configuration)
        self._card_search_flow.delegate = self
        
        self._resource_deployer = ImageResourceDeployer(configuration)
        self._resource_deployer.delegate = self
        
        self._observation_tower = observation_tower
        self.delegate = None
        
    @property
    def card_search_flow(self) -> CardSearchFlow:
        return self._card_search_flow

    @property
    def resource_deployer(self) -> ImageResourceDeployer:
        return self._resource_deployer

    # MARK: - DS Delegate methods
    def sf_did_complete_search(self, cs: CardSearchFlow, result_list: List[TradingCard], error: Exception):
        display_name_list = list(map(lambda x: x.friendly_display_name, result_list))
        self.delegate.app_did_complete_search(self, display_name_list, error)

    def sf_did_retrieve_card_resource_for_card_selection(self, cs: CardSearchFlow, trading_card: TradingCard):
        self.delegate.app_did_retrieve_card_resource_for_card_selection(self, trading_card.local_resource, trading_card.is_flippable)

    # MARK: - Resource Cacher Delegate
    def sf_did_finish_storing_local_resource(self, sf: CardSearchFlow, local_resource: LocalCardResource):
        self._retrieve_publish_status_and_notify_if_needed()

    def _retrieve_publish_status_and_notify_if_needed(self):
        publish_status = self._resource_deployer.can_publish_staged_resources()
        self.delegate.app_publish_status_changed(publish_status)
    


    # MARK: - Resource manager
    def can_stage_current_card_search_resource_to_stage_index(self, index: int) -> bool:
        return self._card_search_flow.current_card_search_resource is not None and index < len(self._resource_deployer.production_resources)

    def stage_resource(self, index: int):
        if self._card_search_flow.current_card_search_resource is not None:
            self._resource_deployer.stage_resource(self._card_search_flow.current_card_search_resource, index)
            self._retrieve_publish_status_and_notify_if_needed()

    def unstage_resource(self, index: int):
        self._resource_deployer.unstage_resource(index)
        self._retrieve_publish_status_and_notify_if_needed()

    def unstage_all_resources(self):
        self._resource_deployer.unstage_all_resources()
        self._retrieve_publish_status_and_notify_if_needed()

    def load_production_resources(self):
        self._resource_deployer.load_production_resources()

    def can_publish_staged_resources(self) -> bool:
        return self._resource_deployer.can_publish_staged_resources()

    def publish_staged_resources(self) -> bool:
        return self._resource_deployer.publish_staged_resources()
    
    # MARK: - Resource Deployer Delegate methods
    def rm_did_load_production_resources(self, rm: ImageResourceDeployer, production_resources: List[LocalCardResource]):
        self.delegate.app_did_load_production_resources(self, production_resources)