from datetime import date, datetime
from typing import List, Dict
from uuid import UUID

from pydantic import BaseModel, PositiveInt

from bigchain.types import Mark


class BigchainSettings(BaseModel):
    rpc: str


class AcademicTranscription(BaseModel):
    on_date: date
    student_id: UUID
    subject_id: PositiveInt
    subject_type_id: PositiveInt
    mark: Mark
    additional_info: str
    organization_id: PositiveInt
    semester: PositiveInt
    hours: PositiveInt
    version: int

    @classmethod
    def from_bigchain(cls, data):
        return AcademicTranscription(
            on_date=datetime.strptime(data['OnDate'], '%Y-%m-%dT%H:%M:%S'),
            student_id=data['StudentId'],
            subject_id=data['SubjectId'],
            subject_type_id=data['SubjectTypeId'],
            mark=data['Mark'],
            additional_info=data['AdditionalInfo'],
            organization_id=data['OrganizationId'],
            semester=data['Semester'],
            hours=data['Hours'],
            version=data['Version'],
        )


class AcademicSummarySubject(BaseModel):
    hours: PositiveInt
    marks: List[Mark]


class AcademicSummary(BaseModel):
    summary: Dict[PositiveInt, AcademicSummarySubject]
