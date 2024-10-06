import requests
from PyQt5 import *
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore

# multithreading
# https://stackoverflow.com/questions/6783194/background-thread-with-qthread-in-pyqt
# https://gist.github.com/d-kozak/0474294db8b60b7b12d146cc0658baf8

class MainProgramViewController(QWidget):
    def __init__(self, 
                card_search_view,
                deployment_view,
                data_source, 
                resource_manager):
        super().__init__()

        

        box = QHBoxLayout()
        layout = QSplitter(QtCore.Qt.Horizontal)
        
        box.addWidget(layout)
        self.setLayout(box)

        card_search_view.delegate = self
        self.card_search_view = card_search_view
        layout.addWidget(card_search_view)

        deployment_view.delegate = self
        self.deployment_view = deployment_view
        layout.addWidget(deployment_view)
        layout.setSizes([75,400])
        data_source.delegate = self
        self.data_source = data_source

        resource_manager.delegate = self
        self.resource_manager = resource_manager

        self.current_card_search_resource = None

        # self.poll_for_image()

    def load(self):
        self.resource_manager.load_production_resources()

    def poll_for_image(self):
        print("polling")
        # https://www.reddit.com/r/learnpython/comments/392hkp/best_way_to_poll_for_new_data_tkinter/
        # self.data_source.retrieve_prod_image()
        self.after(1000 * 6, self.poll_for_image)

    # resource manager
    def rm_did_load_production_resources(self, rm, production_resources):
        self.deployment_view.clear_list()
        for i in production_resources:
            img_qp = QPixmap()
            img_qp.load(i.image_preview_path)
            file_name = i.file_name
            staging_button_enabled = self.current_card_search_resource is not None
            self.deployment_view.create_list_item(f'File: {file_name}', file_name, img_qp, staging_button_enabled)

    # search table view
    def tv_did_tap_search(self, table_view, query):
        self.data_source.search(query)

    def tv_did_select(self, table_view, index):
        self.data_source.select_card_resource_for_card_selection(index)
        self.deployment_view.set_all_staging_button_enabled(True)

    def cs_did_tap_flip_button(self, cs):
        self.data_source.flip_current_previewed_card()

    # image deployment view
    def idl_did_tap_staging_button(self, id_list, id_cell, index):
        img_qp = QPixmap()
        img_qp.load(self.current_card_search_resource.image_preview_path)
        self.deployment_view.set_staging_image(self.current_card_search_resource.display_name, img_qp, index)
        self.resource_manager.stage_resource(self.current_card_search_resource, index)
        self.deployment_view.set_production_button_enabled(True)

    def idl_did_tap_unstaging_button(self, id_list, id_cell, index):
        self.deployment_view.clear_staging_image(index)
        self.resource_manager.unstage_resource(index)
        self.deployment_view.set_production_button_enabled(False)

    def idl_did_tap_unstage_all_button(self):
        self.deployment_view.clear_all_staging_images()
        self.resource_manager.unstage_all_resources()

    def idl_did_tap_production_button(self):
        self.resource_manager.publish_staged_resources()
        self.deployment_view.clear_all_staging_images()
        self.resource_manager.load_production_resources()
        self.deployment_view.set_production_button_enabled(False)

    # data source
    def ds_completed_search_with_result(self, ds, result_list, error):
        self.card_search_view.update_list(result_list)

    def ds_did_retrieve_card_resource_for_card_selection(self, ds, remote_card_resource, is_flippable):
        local_card_resource = self.resource_manager.generate_local_card_resource(remote_card_resource)
        img_qp = QPixmap()
        img_qp.load(local_card_resource.image_preview_path)
        self.card_search_view.set_image(remote_card_resource.display_name, img_qp, is_flippable)
        self.current_card_search_resource = local_card_resource