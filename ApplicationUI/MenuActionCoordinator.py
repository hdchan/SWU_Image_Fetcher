class MenuActionCoordinator:
    def __init__(self, 
                 main_program, 
                 resource_manager,
                 configuration,
                 configuration_manager):
        self.main_program = main_program
        self.resource_manager = resource_manager
        self.configuration = configuration
        self.configuration_manager = configuration_manager

    def did_input_new_file_name(self, file_name):
        self.resource_manager.generate_new_file(file_name)
        self.main_program.load()

    def did_tap_refresh_production_images(self):
        self.main_program.load()

    def did_toggle_performance_mode(self, is_on):
        self.configuration_manager.toggle_performance_mode(is_on)
