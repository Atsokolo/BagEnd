from pydantic import BaseModel, ConfigDict
from typing import Optional

# Схема для создания/обновления издателя
class PublisherCreateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    names: str
    address:str # Адрес может быть необязательным
    phone_number: str  # Номер телефона может быть необязательным
    email:str # Email может быть необязательным

# Схема для издателя с идентификатором (для данных из базы)
class PublisherSchema(PublisherCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int  # Поле с идентификатором для сохранённых издателей