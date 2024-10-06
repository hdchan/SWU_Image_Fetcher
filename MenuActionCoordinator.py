from PyQt5 import *
from PyQt5.QtWidgets import QMessageBox


class MenuActionCoordinator:
    def __init__(self, main_program, resource_manager, configuration_manager):
        self.main_program = main_program
        self.resource_manager = resource_manager
        self.configuration_manager = configuration_manager

    def did_input_new_file_name(self, file_name):
        try:
            self.resource_manager.generate_new_file(file_name)
            self.main_program.load()
        except Exception as error:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(str(error))
            msgBox.setWindowTitle("Error")
            msgBox.setStandardButtons(QMessageBox.Ok)

            returnValue = msgBox.exec()
            # if returnValue == QMessageBox.Ok:
            #     print('OK clicked')

    def did_tap_refresh_production_images(self):
        self.main_program.load()

    def did_toggle_performance_mode(self, is_on):
        self.configuration_manager.toggle_performance_mode(is_on)