from PyQt5 import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class CardSearchPreviewViewController(QWidget):
    def __init__(self, preview_view, search_table_view):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        preview_view.delegate = self
        self.staging_view = preview_view
        layout.addWidget(preview_view)

        flip_button = QPushButton()
        flip_button.setText("Flip")
        flip_button.setEnabled(False)
        flip_button.clicked.connect(self.tapped_flip_button)
        self.flip_button = flip_button
        layout.addWidget(flip_button)
        

        search_table_view.delegate = self
        self.search_table_view = search_table_view
        layout.addWidget(search_table_view)

    @property
    def delegate(self):
        return self._delegate
    
    @delegate.setter
    def delegate(self, value):
        self._delegate = value
        self.search_table_view.delegate = value
        self.staging_view.delgate = value

    def set_image(self, text, img, is_flippable):
        self.staging_view.set_image(text, img)
        self.flip_button.setEnabled(is_flippable)

    def update_list(self, result_list):
        self.search_table_view.update_list(result_list)

    def tapped_flip_button(self):
        self.delegate.cs_did_tap_flip_button(self)