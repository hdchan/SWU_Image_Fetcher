from PyQt5 import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5 import QtCore
from EventBus import EventBus, ConfigurationUpdatedEvent

class ImagePreviewViewController(QWidget):
    def __init__(self, event_bus):
        super().__init__()
        self.event_bus = event_bus
        layout = QVBoxLayout(self)
        
        label = QLabel(self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

        self.image_view = label
        self.current_image = None

        self.event_bus.subscribe(self, ConfigurationUpdatedEvent)

    def set_image(self, img_alt, image = None):
        self.current_image = None
        if image is not None:
            self.image_view.setPixmap(image)
            self.current_image = image
        else:   
            self.image_view.setText(img_alt)

    def clear_image(self):
        self.image_view.clear()

    def handle_event_bus_event(self, event):
        # event.configuration.is_performance_mode_on
        pass