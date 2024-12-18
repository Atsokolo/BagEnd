from pydantic import BaseModel, ConfigDict
from typing import Optional

# Схема для создания/обновления записи в Discount_list
class DiscountListCreateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book_id: int  # Идентификатор книги
    discount_id: int  # Идентификатор скидки

# Схема для Discount_list с идентификатором (для данных из базы)
class DiscountListSchema(DiscountListCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int  # Поле с идентификатором для сохранённых связей в Discount_list
