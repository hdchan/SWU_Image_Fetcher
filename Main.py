
from PyQt5 import *
from PyQt5.QtWidgets import QApplication
from Window import Window
from MenuActionCoordinator import MenuActionCoordinator
from CardSearchPreviewViewController import CardSearchPreviewViewController
from MainProgramViewController import MainProgramViewController
from SearchTableView import SearchTableView
from ImagePreviewViewController import ImagePreviewViewController
from ImageDeploymentListViewController import ImageDeploymentListViewController
from DataSource import DataSource
from ImageResourceManager import ImageResourceManager
from EventBus import EventBus
from ConfigurationManager import ConfigurationManager

app = QApplication([])
event_bus = EventBus()
configuration_manager = ConfigurationManager(event_bus=event_bus)
card_search_widget = CardSearchPreviewViewController(ImagePreviewViewController(event_bus=event_bus),
                                                     SearchTableView())
image_resource_manager = ImageResourceManager()
main_window = Window()
main_program = MainProgramViewController(card_search_widget,
                                   ImageDeploymentListViewController(event_bus=event_bus),
                                   DataSource(), 
                                   image_resource_manager)
main_program.load()
menu_coordinator = MenuActionCoordinator(main_program, 
                                         image_resource_manager, 
                                         configuration_manager=configuration_manager)
main_window.setCentralWidget(main_program)
main_window.delegate = menu_coordinator
main_window.show()
app.exec()