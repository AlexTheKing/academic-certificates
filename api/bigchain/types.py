from enum import Enum

from pydantic import conint

Mark = conint(ge=0, le=10)


class AssetType(str, Enum):
    DIPLOMA = 'diploma'
    TRANSCRIPTION = 'transcription'


class Mark(str, Enum):
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    PASSED = 'passed'
    NOT_PASSED = 'not_passed'
