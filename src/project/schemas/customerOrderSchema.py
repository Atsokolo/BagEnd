from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

# Схема для создания/обновления заказа
class CustomerOrderCreateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    discount_id: int  # Идентификатор скидки, может быть пустым
    customer_id: int  # Идентификатор клиента
    order_date: date  # Дата заказа
    total: float  # Общая сумма заказа
    status: int  # Статус заказа (например, 1 - активен, 0 - завершён)

# Схема для извлечения информации о заказах с id
class CustomerOrderSchema(CustomerOrderCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int  # Идентификатор заказа в базе данных
