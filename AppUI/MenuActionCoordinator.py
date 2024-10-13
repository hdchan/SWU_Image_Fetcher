from AppCore.Image.ImageResourceManager import ImageResourceManager
from AppCore.Config.ConfigurationManager import ConfigurationManager
class MenuActionCoordinator:
    def __init__(self, 
                 main_program, 
                 resource_manager: ImageResourceManager,
                 configuration_manager: ConfigurationManager):
        self.main_program = main_program
        self.resource_manager = resource_manager
        self.configuration_manager = configuration_manager

    def did_input_new_file_name(self, file_name: str):
        self.resource_manager.generate_new_file(file_name)
        self.main_program.load()

    def did_tap_refresh_production_images(self):
        self.main_program.load()

    def did_toggle_performance_mode(self, is_on: bool):
        self.configuration_manager.toggle_performance_mode(is_on)

    def did_toggle_mock_data_mode(self, is_on: bool):
        self.configuration_manager.toggle_mock_data_mode(is_on)
