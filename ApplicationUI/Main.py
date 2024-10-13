
from PyQt5 import *
from PyQt5.QtWidgets import QApplication

from ApplicationCore import App
from ApplicationCore.Configuration import ConfigurationManager, Configuration
from ApplicationCore.Observation.ObservationTower import ObservationTower
from ApplicationUI.MainProgramViewController import MainProgramViewController
from ApplicationUI.MenuActionCoordinator import MenuActionCoordinator
from ApplicationUI.Window import Window


def main():
    app = QApplication([])
    observation_tower = ObservationTower()
    configuration = Configuration()
    configuration_manager = ConfigurationManager(observation_tower, 
                                                 configuration)
    application_core = App(observation_tower, configuration)
    main_window = Window(configuration)
    main_program = MainProgramViewController(observation_tower,
                                             configuration,
                                             application_core)
    main_program.load()
    menu_coordinator = MenuActionCoordinator(main_program, 
                                             application_core._resource_manager,
                                             configuration,
                                             configuration_manager)
    main_window.setCentralWidget(main_program)
    main_window.delegate = menu_coordinator
    main_window.show()
    app.exec()