from typing import Dict, Any

class Configuration:
    class Toggles:
        def __init__(self):
            self.developer_mode = False
            
    class Settings:
        def __init__(self):
            self.is_mock_data = False
            self.is_performance_mode = False

    def __init__(self):
        self._app_display_name = 'R4-MG'
        self._app_ui_version = '0.2.0'
        self._app_core_version = '0.2.0'

        self._toggles = Configuration.Toggles()
        self._settings = Configuration.Settings()

    @property
    def app_display_name(self):
        if self.is_developer_mode:
            return self._app_display_name + " [DEVELOPER MODE]"
        else:
            return self._app_display_name

    @property
    def app_ui_version(self):
        return self._app_ui_version
    
    @property
    def is_performance_mode(self) -> bool:
        return self._settings.is_performance_mode
    
    @is_performance_mode.setter
    def is_performance_mode(self, value: bool):
        self._settings.is_performance_mode = value

    @property
    def is_developer_mode(self) -> bool:
        return self._toggles.developer_mode

    @property
    def is_mock_data(self) -> bool:
        if self.is_developer_mode:
            return self._settings.is_mock_data
        else:
            return False
    
    @is_mock_data.setter
    def is_mock_data(self, value: bool):
        self._settings.is_mock_data = value

    def loadJSON(self, json: Dict[str, Any]):
        toggles = json.get('toggles', {})
        if toggles is None:
            toggles = {}
        settings = json.get('settings', {})
        if settings is None:
            settings = {}
        
        self._toggles.developer_mode = toggles.get('developer_mode', False)
        
        self._settings.is_mock_data = settings.get('is_mock_data', False)
        self._settings.is_performance_mode = settings.get('is_performance_mode', False)

    def toJSON(self) -> Dict[str, object]:
        config: Dict[str, object] = {
            "toggles": {
            },
            "settings": {
                "is_performance_mode": self.is_performance_mode
            }
        }
        if self._toggles.developer_mode:
            config['toggles']['developer_mode'] = self._toggles.developer_mode
            config['settings']['is_mock_data'] = self._settings.is_mock_data
        return config

