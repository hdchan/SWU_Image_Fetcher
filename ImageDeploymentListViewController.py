from PyQt5 import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton

from ImageDeploymentViewController import ImageDeploymentViewController


class ImageDeploymentListViewController(QWidget):
    def __init__(self, event_bus):
        super().__init__()

        self.event_bus = event_bus

        layout = QVBoxLayout()
        scroll = QScrollArea(self)
        widget = QWidget()
        widget.setLayout(layout)
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        layout_2 = QVBoxLayout()
        layout_2.addWidget(scroll)

        unstage_all_button = QPushButton()
        unstage_all_button.setText("Unstage All")
        unstage_all_button.setEnabled(False)
        unstage_all_button.clicked.connect(self.tapped_unstage_all_button)
        self.unstage_all_button = unstage_all_button
        # layout_2.addWidget(unstage_all_button)

        production_button = QPushButton()
        production_button.setText("Production")
        production_button.setEnabled(False)
        production_button.clicked.connect(self.tapped_production_button)
        production_button.setStyleSheet("background-color : #90EE90")
        self.production_button = production_button
        layout_2.addWidget(production_button)

        self.setLayout(layout_2)

        self.layout = layout
        self.list_items = []
        self.scroll = scroll
        self.delegate = None

    def create_list_item(self, file_name, img_alt, img, staging_button_enabled):
        item = ImageDeploymentViewController(self.event_bus)
        item.delegate = self
        item.set_production_image(img_alt, img)
        item.set_label(file_name)
        item.set_staging_button_enabled(staging_button_enabled)
        self.layout.addWidget(item)

        self.list_items.append(item)

    def clear_list(self):
        for i in reversed(range(self.layout.count())):
            self.layout.takeAt(i).widget().deleteLater()
        self.list_items = []

    def id_did_tap_staging_button(self, id_cell):
        for idx, i in enumerate(self.list_items):
            if i == id_cell:
                self.delegate.idl_did_tap_staging_button(self, id_cell, idx)

    def id_did_tap_unstaging_button(self, id_cell):
        for idx, i in enumerate(self.list_items):
            if i == id_cell:
                self.delegate.idl_did_tap_unstaging_button(self, id_cell, idx)

    def set_staging_image(self, text, img, index):
        self.list_items[index].set_staging_image(text, img)

    def clear_staging_image(self, index):
        self.list_items[index].clear_staging_image()
    
    def set_production_image(self, text, img, index):
        self.list_items[index].set_production_image(text, img)

    def clear_all_staging_images(self):
        for idx, i in enumerate(self.list_items):
            i.clear_staging_image()

    def tapped_production_button(self):
        self.delegate.idl_did_tap_production_button()

    def tapped_unstage_all_button(self):
        self.delegate.idl_did_tap_unstage_all_button()

    def set_all_staging_button_enabled(self, enabled):
        for idx, i in enumerate(self.list_items):
            i.set_staging_button_enabled(enabled)

    def set_production_button_enabled(self, enabled):
        self.production_button.setEnabled(enabled)