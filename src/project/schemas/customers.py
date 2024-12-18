from pydantic import BaseModel, Field, ConfigDict


class CustomersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    address: str
    email: str
    password: str
    phone_number: str | None = Field(default=None)

class CustomersCreateSchema(BaseModel):
    login: str
    address: str
    email: str
    password: str
    phone_number: str | None = Field(default=None)



