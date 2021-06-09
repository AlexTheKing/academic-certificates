import time

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from web3 import Web3
from web3.contract import Contract, ContractFunction
from web3.exceptions import ContractLogicError

from dependencies import get_account_credentials, get_contract, get_web3, get_settings
from ethereum.account.models import AccountCredentials
from ethereum.contract.models import Certificate
from ethereum.contract.types import String16
from ethereum.models import Settings
from ethereum.types import Hash

app = FastAPI()


@app.exception_handler(ContractLogicError)
def contract_logic_error_handler(request: Request, error: ContractLogicError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=dict(error=error.args[0].split('revert ')[-1])
    )


@app.post('/certificates', status_code=201)
def issue_certificate(certificate: Certificate, web3: Web3 = Depends(get_web3),
                      contract: Contract = Depends(get_contract),
                      account_credentials: AccountCredentials = Depends(get_account_credentials),
                      settings: Settings = Depends(get_settings)) -> Hash:
    if account_credentials.is_supervisor:
        contract_function = contract.functions.issueBySupervisor
        parameters = [
            certificate.number,
            certificate.student.full_name,
            certificate.student.guid,
            certificate.type,
            int(time.mktime(certificate.registration_date.timetuple())),
            int(time.mktime(certificate.release_date.timetuple())),
            certificate.organization,
            certificate.place_of_issue,
            certificate.additional_info
        ]
    else:
        contract_function = contract.functions.issueByRegulator
        parameters = [
            certificate.number,
            certificate.student.full_name,
            certificate.student.guid,
            certificate.type,
            int(time.mktime(certificate.registration_date.timetuple())),
            int(time.mktime(certificate.release_date.timetuple())),
            certificate.place_of_issue,
            certificate.additional_info
        ]
    function = contract_function(*parameters)
    return execute_contract_function(function, web3, account_credentials, settings)


@app.post('/certificates/{certificate_id}/cancel')
def cancel_certificate(certificate_id: String16, web3: Web3 = Depends(get_web3),
                       contract: Contract = Depends(get_contract),
                       account_credentials: AccountCredentials = Depends(get_account_credentials),
                       settings: Settings = Depends(get_settings)) -> Hash:
    function = contract.functions.cancel(certificate_id)
    return execute_contract_function(function, web3, account_credentials, settings)


def execute_contract_function(function: ContractFunction, web3: Web3, account_credentials: AccountCredentials,
                              settings: Settings) -> Hash:
    nonce = web3.eth.get_transaction_count(account_credentials.address)
    transaction = function.buildTransaction({
        'chainId': settings.chain_id,
        'gas': function.estimateGas({'from': account_credentials.address}),
        'gasPrice': web3.toWei(settings.gas_price, 'gwei'),
        'nonce': nonce
    })
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key=account_credentials.private_key)
    return web3.eth.send_raw_transaction(signed_transaction.rawTransaction).hex()
