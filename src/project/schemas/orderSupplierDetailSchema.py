from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional

# Схема для создания/обновления деталей заказа поставщика
class OrderSupplierDetailsCreateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_publ_id: int  # Идентификатор заказа поставщика
    book_id: int  # Идентификатор книги
    count: int  # Количество
    price_per_unit: Decimal  # Цена за единицу товара

# Схема для извлечения информации о деталях заказа поставщика с id
class OrderSupplierDetailsSchema(OrderSupplierDetailsCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int  # Идентификатор детали заказа
