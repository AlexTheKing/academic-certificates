from pydantic import BaseModel, conint

from ethereum.types import Address


class Settings(BaseModel):
    rpc: str
    contract_address: Address
    gas_price: conint(gt=0)
    chain_id: int
