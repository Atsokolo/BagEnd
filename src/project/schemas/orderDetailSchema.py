from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal

# Схема для создания/обновления деталей заказа
class OrderDetailsCreateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int  # Идентификатор заказа
    book_id: int  # Идентификатор книги
    count: int  # Количество книг в заказе (должно быть больше 0)
    price_per_unit: Decimal  # Цена за единицу книги

# Схема для извлечения информации о деталях заказа с id
class OrderDetailsSchema(OrderDetailsCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int  # Идентификатор детали заказа
