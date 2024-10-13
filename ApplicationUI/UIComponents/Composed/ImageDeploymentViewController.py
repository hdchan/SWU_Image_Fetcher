from PyQt5 import *
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
                             QWidget)

from ApplicationUI.UIComponents import ImagePreviewViewController


class ImageDeploymentViewController(QWidget):
    def __init__(self, observation_tower, configuration):
        super().__init__()

        self.observation_tower = observation_tower

        layout = QHBoxLayout()
        first_column_layout = QVBoxLayout()

        label = QLabel()
        label.setWordWrap(True)
        label.setAlignment(QtCore.Qt.AlignCenter)
        first_column_layout.addWidget(label)
        self.label = label

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

        first_column_widget = QWidget()
        first_column_widget.setMaximumHeight(150)
        first_column_widget.setLayout(first_column_layout)
        first_column_widget.setFixedWidth(150)
        layout.addWidget(first_column_widget)

        

        staging_image_view = ImagePreviewViewController(observation_tower=self.observation_tower, 
                                                        configuration=configuration)
        # staging_image_view.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # staging_image_view.setStyleSheet('background-color: red;')
        layout.addWidget(staging_image_view, 4)
        self.staging_image_view = staging_image_view

        production_image_view = ImagePreviewViewController(observation_tower=self.observation_tower, 
                                                           configuration=configuration)
        layout.addWidget(production_image_view, 4)
        self.production_image_view = production_image_view

        self.setLayout(layout)

        self.delegate = None

    def set_staging_image(self, img_alt, img_path):
        self.staging_image_view.set_image(img_alt, img_path)
        self.unstage_button.setEnabled(True)

    def clear_staging_image(self):
        self.staging_image_view.clear_image()
        self.unstage_button.setEnabled(False)

    def set_production_image(self, img_alt, img_path):
        self.production_image_view.set_image(img_alt, img_path)

    def set_label(self, text):
        self.label.setText(text)

    def tapped_staging_button(self):
        self.delegate.id_did_tap_staging_button(self)

    def set_staging_button_enabled(self, enabled):
        self.stage_button.setEnabled(enabled)

    def tapped_unstaging_button(self):
        self.delegate.id_did_tap_unstaging_button(self)
