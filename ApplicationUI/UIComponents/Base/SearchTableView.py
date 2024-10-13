from PyQt5 import *
from PyQt5.QtWidgets import (QLineEdit, QListWidget, QPushButton, QVBoxLayout,
                             QWidget)

from ApplicationCore.Observation.Events import SearchEvent


class SearchTableView(QWidget):
    def __init__(self, observation_tower):
        super().__init__()
        searchbar = QLineEdit(self)
        searchbar.setPlaceholderText("Search card by name (Ctrl+L)")
        searchbar.returnPressed.connect(self.search)
        self.searchbar = searchbar

        search_button = QPushButton()
        search_button.setText("Search (Enter)")
        search_button.clicked.connect(self.search)
        self.search_button = search_button

        result_list = QListWidget(self)
        result_list.itemSelectionChanged.connect(self.get_selection)
        self.result_list = result_list

        layout = QVBoxLayout(self)
        layout.addWidget(searchbar)
        layout.addWidget(search_button)
        layout.addWidget(result_list)
        self.setLayout(layout)

        self.delegate = None

        
        observation_tower.subscribe(self, SearchEvent)

    def get_selection(self):
        selected_indexs = self.result_list.selectedIndexes()
        if len(selected_indexs) > 0:
            self.delegate.tv_did_select(self, selected_indexs[0].row())

    def set_search_focus(self):
        self.searchbar.setFocus()

    def set_item_active(self, index):
        self.result_list.setCurrentRow(index)

    def search(self, *args):
        # prevent query errors
        stripped_text = self.searchbar.text().strip()
        self.searchbar.setText(stripped_text)
        self.delegate.tv_did_tap_search(self, stripped_text)

    def update_list(self, list):
        self.result_list.clear()
        for i in list:
            self.result_list.addItem(i)

    def handle_observation_tower_event(self, event):
        if event.event_type == SearchEvent.EventType.STARTED:
            self.searchbar.setEnabled(False)
            self.search_button.setEnabled(False)
        elif event.event_type == SearchEvent.EventType.FINISHED:
            self.searchbar.setEnabled(True)
            self.search_button.setEnabled(True)