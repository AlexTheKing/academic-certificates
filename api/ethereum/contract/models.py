from datetime import date

from pydantic import BaseModel

from ethereum.contract.types import String16, String32, String36, String48, String64


class Student(BaseModel):
    full_name: String48
    guid: String36


class Issuer(BaseModel):
    name: String48
    location: String32


class Certificate(BaseModel):
    number: String16
    student: Student
    type: String16
    registration_date: date
    release_date: date
    organization: String48
    place_of_issue: String32
    additional_info: String64


class IssuedCertificate(Certificate):
    issuer: Issuer
    is_cancelled: bool

    @classmethod
    def from_contract(cls, data):
        return IssuedCertificate(
            number=data[0],
            student=Student(
                full_name=data[1][0],
                guid=data[1][1]
            ),
            issuer=Issuer(name=data[2][0], location=data[2][1]),
            type=data[3],
            registration_date=date.fromtimestamp(data[4]),
            release_date=date.fromtimestamp(data[5]),
            organization=data[6],
            place_of_issue=data[7],
            additional_info=data[8],
            is_cancelled=data[9]
        )
