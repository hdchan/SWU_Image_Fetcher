from PyQt5 import *
from PyQt5.QtWidgets import (QAction, QDesktopWidget, QInputDialog,
                             QMainWindow, QMenu, QMenuBar, QMessageBox)

from AppCore.Config import Configuration
from AppCore.Observation.Events import (ConfigurationUpdatedEvent,
                                        TransmissionProtocol)
from AppCore.Observation.ObservationTower import ObservationTower


class Window(QMainWindow):
    def __init__(self, configuration: Configuration, observation_tower: ObservationTower, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.configuration = configuration
        
        self._load_window_title()
        # self.setWindowIcon(QtGui.QIcon('./resources/logo.png'))
        self.setGeometry(0, 0, 1200, 800)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        

        menuBar = QMenuBar(self)
        menuBar.setNativeMenuBar(False)

        # MARK: - File
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)

        new_file_menu = QAction('New image file', self)
        new_file_menu.triggered.connect(self.new_file_tapped)
        fileMenu.addAction(new_file_menu)

        refresh_production_images = QAction('Refresh production images', self)
        refresh_production_images.triggered.connect(self.refresh_production_images_tapped)
        fileMenu.addAction(refresh_production_images)

        performance_mode = QAction('🚗💨', self)
        performance_mode.triggered.connect(self.performance_mode_toggled)
        performance_mode.setCheckable(True)
        performance_mode.setChecked(configuration.is_performance_mode)
        fileMenu.addAction(performance_mode)


        # MARK: - About
        about_menu = QMenu("&About", self)
        menuBar.addMenu(about_menu)

        version_info = QAction(f"v.{self.configuration.app_ui_version}", self)
        version_info.setEnabled(False)
        about_menu.addAction(version_info)

        self.setMenuBar(menuBar)

        # MARK: - Developer
        if self.configuration.is_developer_mode:
            developer_menu = QMenu("&Developer", self)
            menuBar.addMenu(developer_menu)

            mock_data_mode = QAction('Mock data', self)
            mock_data_mode.triggered.connect(self.mock_data_mode_toggled)
            mock_data_mode.setCheckable(True)
            developer_menu.addAction(mock_data_mode)

        observation_tower.subscribe(self, ConfigurationUpdatedEvent)


    def new_file_tapped(self):
        text, ok = QInputDialog.getText(self, 'Create new image file', 'Enter file name:')
        if ok:
            try:
                self.delegate.did_input_new_file_name(text)
            except Exception as error:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText(str(error))
                msgBox.setWindowTitle("Error")
                msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
                msgBox.exec()

    def refresh_production_images_tapped(self):
        self.delegate.did_tap_refresh_production_images()

    def performance_mode_toggled(self, is_on: bool):
        self.delegate.did_toggle_performance_mode(is_on)

    def mock_data_mode_toggled(self, is_on: bool):
        self.delegate.did_toggle_mock_data_mode(is_on)

    def _load_window_title(self):
        self.setWindowTitle(self.configuration.app_display_name)

    def handle_observation_tower_event(self, event: TransmissionProtocol):
        self._load_window_title()