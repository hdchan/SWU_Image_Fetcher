from PyQt5 import *
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5 import QtCore
from ImagePreviewViewController import ImagePreviewViewController


class ImageDeploymentViewController(QWidget):
    def __init__(self, event_bus):
        super().__init__()

        self.event_bus = event_bus

        layout = QHBoxLayout()
        first_column_layout = QVBoxLayout()

        stage_button = QPushButton()
        stage_button.setText("Stage")
        stage_button.clicked.connect(self.tapped_staging_button)
        stage_button.setEnabled(False)
        self.stage_button = stage_button
        first_column_layout.addWidget(stage_button)

        unstage_button = QPushButton()
        unstage_button.setText("Unstage")
        unstage_button.clicked.connect(self.tapped_unstaging_button)
        unstage_button.setEnabled(False)
        self.unstage_button = unstage_button
        first_column_layout.addWidget(unstage_button)


        layout.addLayout(first_column_layout)

        label = QLabel()
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label, 1)
        self.label = label

        staging_image_view = ImagePreviewViewController(event_bus=self.event_bus)
        # staging_image_view.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # staging_image_view.setStyleSheet('background-color: red;')
        layout.addWidget(staging_image_view, 4)
        self.staging_image_view = staging_image_view

        production_image_view = ImagePreviewViewController(event_bus=self.event_bus)
        layout.addWidget(production_image_view, 4)
        self.production_image_view = production_image_view

        self.setLayout(layout)

        self.delegate = None

    def set_staging_image(self, img_alt, img):
        self.staging_image_view.set_image(img_alt, img)
        self.unstage_button.setEnabled(True)

    def clear_staging_image(self):
        self.staging_image_view.clear_image()
        self.unstage_button.setEnabled(False)

    def set_production_image(self, img_alt, img):
        self.production_image_view.set_image(img_alt, img)

    def set_label(self, text):
        self.label.setText(text)

    def tapped_staging_button(self):
        self.delegate.id_did_tap_staging_button(self)

    def set_staging_button_enabled(self, enabled):
        self.stage_button.setEnabled(enabled)

    def tapped_unstaging_button(self):
        self.delegate.id_did_tap_unstaging_button(self)
