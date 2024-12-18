from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class AuthorCreateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    date_of_birth: date

class AuthorSchema(AuthorCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int

