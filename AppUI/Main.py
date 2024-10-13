
from PyQt5.QtWidgets import QApplication

from AppCore import ApplicationCore
from AppCore.Config import ConfigurationManager
from AppCore.Data import APIClientProvider
from AppCore.Image import ImageFetcherProvider
from AppCore.Observation.ObservationTower import ObservationTower
from AppUI.MainProgramViewController import MainProgramViewController
from AppUI.MenuActionCoordinator import MenuActionCoordinator
from AppUI.Window import Window


def main():
    app = QApplication([])
    observation_tower = ObservationTower()
    configuration_manager = ConfigurationManager(observation_tower)
    configuration = configuration_manager.configuration
    api_client_provider = APIClientProvider(configuration)
    image_fetcher_provider = ImageFetcherProvider(configuration)
    
    application_core = ApplicationCore(observation_tower, 
                                       api_client_provider, 
                                       image_fetcher_provider)
    main_window = Window(configuration, 
                         observation_tower)
    main_program = MainProgramViewController(observation_tower,
                                             configuration,
                                             application_core)
    main_program.load()
    menu_coordinator = MenuActionCoordinator(main_program, 
                                             application_core.resource_manager,
                                             configuration_manager)
    main_window.setCentralWidget(main_program)
    main_window.delegate = menu_coordinator
    main_window.show()
    app.exec()