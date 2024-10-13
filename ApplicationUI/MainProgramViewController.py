from PyQt5 import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QSplitter, QWidget, QShortcut
from PyQt5.QtGui import QKeySequence
from ApplicationUI.UIComponents import (CardSearchPreviewViewController,
                                        ImageDeploymentListViewController)
from functools import partial

class MainProgramViewController(QWidget):
    def __init__(self,
                 observation_tower,
                 configuration,
                 application_core):
        super().__init__()

        application_core.delegate = self
        self.application_core = application_core

        box = QHBoxLayout()
        layout = QSplitter(QtCore.Qt.Horizontal)
        
        box.addWidget(layout)
        self.setLayout(box)

        card_search_view = CardSearchPreviewViewController(observation_tower=observation_tower, 
                                                           configuration=configuration)
        card_search_view.delegate = self
        self.card_search_view = card_search_view
        self.card_search_view.set_search_focus()
        layout.addWidget(card_search_view)

        deployment_view = ImageDeploymentListViewController(observation_tower=observation_tower, 
                                                            configuration=configuration)
        deployment_view.delegate = self
        self.deployment_view = deployment_view
        layout.addWidget(deployment_view)
        layout.setSizes([150,400])

        # Needs to block ability to publish if not able to
        self.production_shortcut = QShortcut(QKeySequence(Qt.Modifier.CTRL + Qt.Key.Key_P), self)
        self.production_shortcut.activated.connect(self.idl_did_tap_production_button)

        self.search_shortcut = QShortcut(QKeySequence(Qt.Modifier.CTRL + Qt.Key.Key_L), self)
        self.search_shortcut.activated.connect(self.card_search_view.set_search_focus)

        self.flip_shortcut = QShortcut(QKeySequence(Qt.Modifier.CTRL + Qt.Key.Key_F), self)
        self.flip_shortcut.activated.connect(self._flip_current_previewed_card_if_possible)

        key_pad = [
            Qt.Key.Key_1,
            Qt.Key.Key_2,
            Qt.Key.Key_3,
            Qt.Key.Key_4,
            Qt.Key.Key_5,
            Qt.Key.Key_6,
            Qt.Key.Key_7,
            Qt.Key.Key_8,
            Qt.Key.Key_9,
            Qt.Key.Key_0,
        ]
        for i, k in enumerate(key_pad):
            self.staging_shortcut = QShortcut(QKeySequence(Qt.Modifier.CTRL + k), self)
            self.staging_shortcut.activated.connect(partial(self._stage_current_card_search_resource, i))

    def _stage_current_card_search_resource(self, index):
        if self.application_core.can_stage_current_card_search_resource_to_stage_index(index):
            self.deployment_view.set_staging_image(self.application_core.current_card_search_resource.display_name, self.application_core.current_card_search_resource.image_preview_path, index)
            self.application_core.stage_resource(index)

    def load(self):
        self.application_core.load_production_resources()

    # app core
    def app_did_load_production_resources(self, app, card_resource):
        self.deployment_view.clear_list()
        for index, r in enumerate(card_resource):
            file_name = r.file_name
            staging_button_enabled = self.application_core.current_card_search_resource is not None
            self.deployment_view.create_list_item(f'File: {file_name}', file_name, r.image_preview_path, staging_button_enabled, index)

    def app_did_complete_search(self, app, result_list, error):
        self.card_search_view.update_list(result_list)
        if len(result_list) > 0:
            self.card_search_view.set_item_active(0)

    def app_did_retrieve_card_resource_for_card_selection(self, app, card_resource, is_flippable):
        self.card_search_view.set_image(card_resource.display_name, card_resource.image_preview_path, is_flippable)

    def app_publish_status_changed(self, is_ready):
        self._update_production_button_state()

    # search table view
    def tv_did_tap_search(self, table_view, query):
        self.application_core.search(query)
        

    def tv_did_select(self, table_view, index):
        self.application_core.select_card_resource_for_card_selection(index)
        self.deployment_view.set_all_staging_button_enabled(True)

    # card search
    def cs_did_tap_flip_button(self, cs):
        self._flip_current_previewed_card_if_possible()


    # image deployment view
    def idl_did_tap_staging_button(self, id_list, id_cell, index):
        self._stage_current_card_search_resource(index)

    def idl_did_tap_unstaging_button(self, id_list, id_cell, index):
        self.deployment_view.clear_staging_image(index)
        self.application_core.unstage_resource(index)
        self._update_production_button_state()

    def idl_did_tap_unstage_all_button(self):
        self.deployment_view.clear_all_staging_images()
        self.application_core.unstage_all_resources()

    def idl_did_tap_production_button(self):
        if self.application_core.can_publish_staged_resources():
            publish_success = self.application_core.publish_staged_resources()
            if  publish_success:
                self.application_core.load_production_resources()
                self._update_production_button_state()
                return

    def _update_production_button_state(self):
        production_button_enabled = self.application_core.can_publish_staged_resources()
        self.deployment_view.set_production_button_enabled(production_button_enabled)

    def _flip_current_previewed_card_if_possible(self):
        if self.application_core.current_previewed_response_card_is_flippable():
            self.application_core.flip_current_previewed_card()