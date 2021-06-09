from collections import defaultdict
from uuid import UUID

from bigchaindb_driver import BigchainDB
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from web3.contract import Contract
from web3.exceptions import ContractLogicError

from bigchain.models import AcademicTranscription, AcademicSummary
from bigchain.types import AssetType
from dependencies import get_contract, get_bigchain
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


@app.get('/summary/{student_id}')
def get_certificate_summary(student_id: UUID,
                            bigchain: BigchainDB = Depends(get_bigchain)) -> AcademicSummary:
    assets = bigchain.assets.get(search=student_id)
    transcriptions = (AcademicTranscription.from_bigchain(asset['data'])
                      for asset in assets if asset['data']['Type'] == AssetType.TRANSCRIPTION)
    transcriptions_by_subject = defaultdict(list)
    for transcription in transcriptions:
        transcriptions_by_subject[(transcription.subject_id, transcription.semester)].append(transcription)
    summary = defaultdict(lambda: dict(hours=0, marks=[]))
    for (subject, semester), transcriptions in transcriptions_by_subject.items():
        last_transcription = max(transcriptions, key=lambda transcription: transcription.version)
        summary[subject]['hours'] += last_transcription.hours
        summary[subject]['marks'].append(last_transcription.mark)
    return AcademicSummary(summary=summary)
