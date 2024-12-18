from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class GenreSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

