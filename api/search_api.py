from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from web3.contract import Contract
from web3.exceptions import ContractLogicError

from dependencies import get_contract
from ethereum.contract.models import IssuedCertificate
from ethereum.contract.types import String16

app = FastAPI()


@app.exception_handler(ContractLogicError)
def contract_logic_error_handler(request: Request, error: ContractLogicError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=dict(error=error.args[0].split('revert ')[-1])
    )


@app.get('/certificates/{certificate_number}')
def get_certificate(certificate_number: String16, contract: Contract = Depends(get_contract)) -> IssuedCertificate:
    contract_data = contract.functions.getCertificateById(certificate_number).call()
    print(contract_data)
    return IssuedCertificate.from_contract(contract_data)
