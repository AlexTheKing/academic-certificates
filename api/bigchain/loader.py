import os.path

from bigchain.models import BigchainSettings
from util.loader import JsonLoader


class BigchainSettingsLoader(JsonLoader):
    SETTINGS_FILENAME = 'bigchain_settings.json'
    PATH_TO_SETTINGS = os.path.join('resources', SETTINGS_FILENAME)

    def load(self, *args) -> BigchainSettings:
        return super().load(self.PATH_TO_SETTINGS, BigchainSettings)
