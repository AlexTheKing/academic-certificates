import json
import os.path

from web3 import Web3
from web3.contract import Contract

from ethereum.types import Address


class ContractLoader:
    CONTRACT_ABI_FILENAME = 'AcademicCertificateAuthority.json'
    PATH_TO_ABI = os.path.join('resources', CONTRACT_ABI_FILENAME)

    def __init__(self, web3: Web3):
        self.web3 = web3

    def load(self, address: Address) -> Contract:
        with open(self.PATH_TO_ABI) as file:
            contract_descriptor = json.load(file)
        return self.web3.eth.contract(address=address, abi=contract_descriptor['abi'])
