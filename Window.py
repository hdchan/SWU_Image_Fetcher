from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QAction, QInputDialog, QCheckBox

class Window(QMainWindow):
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.setWindowTitle("RM-4G")
        # self.setWindowIcon(QtGui.QIcon('./resources/logo.png'))

        menuBar = QMenuBar(self)
        menuBar.setNativeMenuBar(False)

        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)

        new_file_menu = QAction('New image file', self)
        new_file_menu.triggered.connect(self.new_file_tapped)
        fileMenu.addAction(new_file_menu)

        refresh_production_images = QAction('Refresh production images', self)
        refresh_production_images.triggered.connect(self.refresh_production_images_tapped)
        fileMenu.addAction(refresh_production_images)

        performance_mode = QAction('📙', self)
        performance_mode.triggered.connect(self.performance_mode_toggled)
        performance_mode.setCheckable(True)
        # fileMenu.addAction(performance_mode)


        self.setMenuBar(menuBar)

    def new_file_tapped(self):
        text, ok = QInputDialog.getText(self, 'Create new image file', 'Enter file name:')
        if ok:
            self.delegate.did_input_new_file_name(text)

    def refresh_production_images_tapped(self):
        self.delegate.did_tap_refresh_production_images()

    def performance_mode_toggled(self, is_on):
        self.delegate.did_toggle_performance_mode(is_on)