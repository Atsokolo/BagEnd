from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import date

# Схема для создания/обновления заказа поставщика
class SupplierOrderCreateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    supplier_id: int  # Идентификатор поставщика
    order_date: date  # Дата заказа
    total: Decimal  # Общая сумма заказа
    status: int  # Статус заказа

# Схема для извлечения информации о заказах поставщика с id
class SupplierOrderSchema(SupplierOrderCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int  # Идентификатор заказа
