
from CardResource import RemoteCardResource
from PyQt5 import QtCore
from SWUCard import SWUCard
from SWUDBClient import SWUDBClient
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

class DataSource:
    def __init__(self):
        self.delegate = None
        self.current_selection = None
        self.current_response_cards = []
        self.current_previewed_card = None
    
    def search(self, query):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.client = SWUDBClient()
        self.client.setQuery(query)
        result = self.client.search()
        self.swu_client_result_ready(result)
        QApplication.restoreOverrideCursor()

    def swu_client_result_ready(self, result):
        """
        called when the computation is finished
        :param result: result of the computation
        """
        # with open('sor.json', 'r') as file:
        #     json_response = json.load(file)
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
            resource = self.retrieve_card_resource(response_card)
            self.delegate.ds_did_retrieve_card_resource_for_card_selection(self, resource, response_card.is_flippable())
            self.current_previewed_card = response_card
    
    def flip_current_previewed_card(self):
        if self.current_previewed_card is not None:
            self.current_previewed_card.flip()
            response_card = self.current_previewed_card
            resource = self.retrieve_card_resource(response_card)
            self.delegate.ds_did_retrieve_card_resource_for_card_selection(self, resource, response_card.is_flippable())
        

    def retrieve_currently_selected_card_resource(self):
        return self.retrieve_card_resource(self.current_previewed_card)

    def retrieve_card_resource(self, response_card):
        img_url = response_card.card_art()
        resource = RemoteCardResource()
        resource.display_name = response_card.friendly_display_name()
        resource.identifier = response_card.unique_identifier()
        resource.image_url = img_url
        return resource
        