from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

# Схема для создания/обновления скидки
class DiscountCreateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    percent: float  # Процент скидки, который не может быть отрицательным
    start_date: Optional[date] = None  # Дата начала скидки (необязательное поле)
    end_date: Optional[date] = None  # Дата окончания скидки (необязательное поле)

# Схема для скидки с идентификатором (для данных из базы)
class DiscountSchema(DiscountCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int  # Поле с идентификатором для сохранённых скидок