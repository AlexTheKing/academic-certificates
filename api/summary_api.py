from collections import defaultdict
from uuid import UUID

from bigchaindb_driver import BigchainDB
from fastapi import FastAPI, Depends

from bigchain.models import AcademicTranscription, AcademicSummary
from bigchain.types import AssetType
from dependencies import get_bigchain

app = FastAPI()


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
