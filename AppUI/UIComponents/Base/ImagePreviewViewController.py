from PyQt5 import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5 import QtCore
from AppCore.Observation.Events import ConfigurationUpdatedEvent, LocalResourceReadyEvent
from PyQt5.QtGui import QPixmap
from .LoadingSpinner import LoadingSpinner

class ImagePreviewViewController(QWidget):
    def __init__(self, observation_tower, configuration):
        super().__init__()
        layout = QVBoxLayout(self)
        
        label = QLabel(self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

        self._image_view = label
        self.loading_spinner = LoadingSpinner(self)

        self._img_path = None
        self._img_alt = None
        self._configuration = configuration

        observation_tower.subscribe(self, ConfigurationUpdatedEvent)
        observation_tower.subscribe(self, LocalResourceReadyEvent)

    def set_image(self, img_alt, img_path):
        self.loading_spinner.start()
        self._img_path = img_path
        self._img_alt = img_alt
        self._load_image_view()

    def clear_image(self):
        self._image_view.clear()
        self._img_path = None
        self._img_alt = None

    def _load_for_configuration(self):
        self._image_view.clear()
        self._load_image_view()

    # async download image https://blog.skyleafdesign.com/how-to-do-concurrent-async-image-download-in-pyqt5/
    def _load_image_view(self):
        if not self._configuration.is_performance_mode:
            if self._img_path is not None:
                image = QPixmap()
                success = image.load(self._img_path)
                if not success:
                    # self._image_view.setText(self._img_alt)
                    self._image_view.clear()
                    self.loading_spinner.start()
                    return
                self._image_view.setPixmap(image)
            self.loading_spinner.stop()
        else:
            self.loading_spinner.stop()
            self._image_view.setText(self._img_alt)

    def handle_observation_tower_event(self, event):
        if type(event) == ConfigurationUpdatedEvent:
            self._load_for_configuration()
        elif type(event) == LocalResourceReadyEvent:
            if self._img_path == event.local_resource.image_preview_path:
                self._load_image_view()
                # TODO: wondering if we can do this differently?
                # maybe register more specific identifiers within the event bus
                print(f"Reloading resource: {self._img_path}")