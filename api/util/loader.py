import json
from typing import TypeVar, Type

from pydantic import BaseModel

Model = TypeVar('Model', bound=BaseModel)


class JsonLoader:
    def load(self, path: str, model: Type[Model]) -> Model:
        with open(path) as file:
            return model(**json.load(file))
