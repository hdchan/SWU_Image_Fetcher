
from configparser import ConfigParser

from .Data import DataSource
from .Observation import ObservationTower
from .Observation.Events import *
from .Utilities import ImageResourceManager


class App:
    def __init__(self, observation_tower, configuration):
        self._data_source = DataSource(configuration)
        self._data_source.delegate = self
        self._resource_manager = ImageResourceManager()
        self._resource_manager.delegate = self
        
        self._observation_tower = observation_tower
        self.current_card_search_resource = None
        self.can_publish = False
        self.delegate = None

        # config = ConfigParser()

        # config.read('config.ini')
        # config.add_section('main')
        # config.set('main', 'key1', 'value1')
        # config.set('main', 'key2', 'value2')
        # config.set('main', 'key3', 'value3')

        # with open('config.ini', 'w') as f:
        #     config.write(f)

    # MARK: - Datasource
    def search(self, query):
        self._observation_tower.notify(SearchEvent(SearchEvent.EventType.STARTED))
        self._data_source.search(query)

    def select_card_resource_for_card_selection(self, index):
        self._data_source.select_card_resource_for_card_selection(index)

    def flip_current_previewed_card(self):
        self._data_source.flip_current_previewed_card()

    def current_previewed_response_card_is_flippable(self):
        return self._data_source.current_previewed_response_card_is_flippable()

    # MARK: - DS Delegate methods
    def ds_completed_search_with_result(self, ds, result_list, error):
        self.delegate.app_did_complete_search(self, result_list, error)
        self._observation_tower.notify(SearchEvent(SearchEvent.EventType.FINISHED))

    def ds_did_retrieve_card_resource_for_card_selection(self, ds, remote_card_resource, is_flippable):
        local_card_resource = self._resource_manager.generate_local_card_resource(remote_card_resource)
        self.delegate.app_did_retrieve_card_resource_for_card_selection(self, local_card_resource, is_flippable)
        self.current_card_search_resource = local_card_resource
    

    # MARK: - Resource manager
    def can_stage_current_card_search_resource_to_stage_index(self, index):
        return self.current_card_search_resource is not None and index < len(self._resource_manager.production_resources)

    def stage_resource(self, index):
        self._resource_manager.stage_resource(self.current_card_search_resource, index)
        self._retrieve_publish_status_and_notify_if_needed()

    def unstage_resource(self, index):
        self._resource_manager.unstage_resource(index)
        self._retrieve_publish_status_and_notify_if_needed()

    def unstage_all_resources(self):
        self._resource_manager.unstage_all_resources()
        self._retrieve_publish_status_and_notify_if_needed()

    def load_production_resources(self):
        self._resource_manager.load_production_resources()


    def can_publish_staged_resources(self):
        return self._resource_manager.can_publish_staged_resources()

    def publish_staged_resources(self):
        return self._resource_manager.publish_staged_resources()


    # MARK: - RM Delegate methods
    def rm_did_load_production_resources(self, rm, production_resources):
        self.delegate.app_did_load_production_resources(self, production_resources)

    def rm_did_finish_storing_local_resource(self, rm, local_resource):
        self._observation_tower.notify(LocalResourceReadyEvent(local_resource))
        self._retrieve_publish_status_and_notify_if_needed()

    
    def _retrieve_publish_status_and_notify_if_needed(self):
        publish_status = self._resource_manager.can_publish_staged_resources()
        # Needs mutex if we're keeping state here
        # if self.can_publish != publish_status:
        self.can_publish = publish_status
        self.delegate.app_publish_status_changed(publish_status)

        