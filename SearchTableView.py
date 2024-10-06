from PyQt5 import *
from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QListWidget

# https://github.com/thom-jp/tkinter_pack_simulator

class SearchTableView(QWidget):
    def __init__(self):
        super().__init__()
        searchbar = QLineEdit(self)
        # searchbar.bind('<KeyRelease>', self.key_released)
        searchbar.returnPressed.connect(self.search)
        self.searchbar = searchbar

        lb = QListWidget(self)
        lb.itemClicked.connect(self.get_selection)
        self.result_list = lb

        layout = QVBoxLayout(self)
        layout.addWidget(searchbar)
        layout.addWidget(lb)
        self.setLayout(layout)

        self.delegate = None

    def get_selection(self, event):
        selected_indexs = self.result_list.selectedIndexes()
        if len(selected_indexs) > 0:
            self.delegate.tv_did_select(self, selected_indexs[0].row())

    def key_released(self, event):
        print(self.searchbar.text())

    def search(self, *args):
        self.delegate.tv_did_tap_search(self, self.searchbar.text())

    def update_list(self, list):
        self.result_list.clear()
        for i in list:
            self.result_list.addItem(i)