from EventBus import ConfigurationUpdatedEvent

class Configuration:
    def __init__(self):
        self.is_perfomance_mode_on = False

class ConfigurationManager:
    def __init__(self, event_bus):
        self.configuration = Configuration()
        self.event_bus = event_bus

    def toggle_performance_mode(self, is_on):
        self.configuration.is_perfomance_mode_on = is_on
        event = ConfigurationUpdatedEvent(configuration=self.configuration)
        self.event_bus.notify(event)

    


