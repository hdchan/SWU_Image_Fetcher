from ApplicationCore.Models import RemoteCardResource
from PyQt5.QtCore import QThread
from .SWUCard import SWUCard
from .SWUDBClient import SWUDBClient, MockSWUClient
from functools import partial

class DataSource:
    def __init__(self, configuration):
        self.configuration = configuration
        self.delegate = None
        self.current_selection = None
        self.current_response_cards = []
        self.current_previewed_response_card = None
        self.latest_thread = None
    
    def search(self, query):
        thread = QThread()
        if self.configuration.is_developer_mode:
            worker = MockSWUClient()
        else:
            worker = SWUDBClient()
        worker.moveToThread(thread)
        # https://realpython.com/python-pyqt-qthread/
        # https://stackoverflow.com/a/50596189
        thread.started.connect(partial(worker.search, query))
        worker.result_available.connect(self.completed_with_search_result)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        self.latest_thread = thread
        thread.start()
        
    def completed_with_search_result(self, result):
        self.current_response_cards = []
        json_response, error = result
        if error is None:
            result_list = []
            for i in json_response['data']:
                swu_card = SWUCard.from_json(i)
                self.current_response_cards.append(swu_card)
                result_list.append(swu_card.friendly_display_name())
            self.delegate.ds_completed_search_with_result(self, result_list, None)
        else: 
            self.delegate.ds_completed_search_with_result(self, [], error)
        
    def select_card_resource_for_card_selection(self, index):
        self.current_selection = index
        if index < len(self.current_response_cards):
            response_card = self.current_response_cards[index]
            resource = self.retrieve_remote_card_resource(response_card)
            self.delegate.ds_did_retrieve_card_resource_for_card_selection(self, resource, response_card.is_flippable())
            self.current_previewed_response_card = response_card

    def current_previewed_response_card_is_flippable(self):
        if self.current_previewed_response_card is not None:
            return self.current_previewed_response_card.is_flippable()
        return False
    
    def flip_current_previewed_card(self):
        if self.current_previewed_response_card is not None and self.current_previewed_response_card_is_flippable():
            self.current_previewed_response_card.flip()
            response_card = self.current_previewed_response_card
            resource = self.retrieve_remote_card_resource(response_card)
            self.delegate.ds_did_retrieve_card_resource_for_card_selection(self, resource, response_card.is_flippable())
        
    def retrieve_currently_selected_card_resource(self):
        return self.retrieve_remote_card_resource(self.current_previewed_response_card)

    def retrieve_remote_card_resource(self, response_card):
        img_url = response_card.card_art()
        resource = RemoteCardResource()
        resource.display_name = response_card.friendly_display_name()
        resource.identifier = response_card.unique_identifier()
        resource.image_url = img_url
        return resource
        