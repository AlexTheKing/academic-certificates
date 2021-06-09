from bigchaindb_driver import BigchainDB
from fastapi import Depends
from web3 import Web3
from web3.contract import Contract

from bigchain.loader import BigchainSettingsLoader
from bigchain.models import BigchainSettings
from ethereum.account.loader import AccountCredentialsLoader
from ethereum.account.models import AccountCredentials
from ethereum.contract.loader import ContractLoader
from ethereum.loader import SettingsLoader
from ethereum.models import Settings


def get_settings() -> Settings:
    return SettingsLoader().load()


def get_web3(settings: Settings = Depends(get_settings)) -> Web3:
    return Web3(Web3.HTTPProvider(settings.rpc))


def get_contract(settings: Settings = Depends(get_settings), web3: Web3 = Depends(get_web3)) -> Contract:
    return ContractLoader(web3).load(settings.contract_address)


def get_account_credentials() -> AccountCredentials:
    return AccountCredentialsLoader().load()


def get_bigchain_settings() -> BigchainSettings:
    return BigchainSettingsLoader().load()


def get_bigchain(bigchain_settings: BigchainSettings = Depends(get_bigchain_settings)) -> BigchainDB:
    return BigchainDB(bigchain_settings.rpc)
