from pydantic import BaseModel

from ethereum.types import Address, Hash


class AccountCredentials(BaseModel):
    address: Address
    private_key: Hash
    is_supervisor: bool
