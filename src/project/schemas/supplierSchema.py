from pydantic import BaseModel, ConfigDict
from typing import Optional

# Схема для создания/обновления поставщика
class SupplierCreateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    names: str  # Название поставщика
    address: Optional[str] = None  # Адрес поставщика (необязательное поле)
    phone_number: Optional[str] = None  # Телефонный номер поставщика (необязательное поле)
    email: Optional[str] = None  # Электронная почта поставщика (необязательное поле)

# Схема для поставщика с идентификатором (для данных из базы)
class SupplierSchema(SupplierCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int  # Поле с идентификатором для сохранённых поставщиков
