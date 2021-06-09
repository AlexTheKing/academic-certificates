import os.path

from ethereum.models import Settings
from util.loader import JsonLoader


class SettingsLoader(JsonLoader):
    SETTINGS_FILENAME = 'settings.json'
    PATH_TO_SETTINGS = os.path.join('resources', SETTINGS_FILENAME)

    def load(self, *args) -> Settings:
        return super().load(self.PATH_TO_SETTINGS, Settings)
