from ApplicationCore.Observation.Events import ConfigurationUpdatedEvent


class ConfigurationManager:
    def __init__(self, observation_tower, configuration):
        self.configuration = configuration
        self.observation_tower = observation_tower

    def toggle_performance_mode(self, is_on):
        self.configuration.is_performance_mode = is_on
        event = ConfigurationUpdatedEvent(configuration=self.configuration)
        self.observation_tower.notify(event)

    


