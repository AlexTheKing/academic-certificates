import os.path

from ethereum.account.models import AccountCredentials
from util.loader import JsonLoader


class AccountCredentialsLoader(JsonLoader):
    ACCOUNT_CREDENTIALS_FILENAME = 'account_credentials.json'
    PATH_TO_CREDENTIALS = os.path.join('resources', ACCOUNT_CREDENTIALS_FILENAME)

    def load(self, *args) -> AccountCredentials:
        return super().load(self.PATH_TO_CREDENTIALS, AccountCredentials)
