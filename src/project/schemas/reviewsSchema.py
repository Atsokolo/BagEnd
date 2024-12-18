from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

# Схема для создания/обновления отзыва
class ReviewCreateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book_id: int  # Идентификатор книги
    customer_id: int  # Идентификатор клиента
    rating: float  # Рейтинг от 0 до 5
    reviews_text: str  # Текст отзыва (необязательное поле)
    date: date  # Дата отзыва

# Схема для отзыва с идентификатором (для данных из базы)
class ReviewSchema(ReviewCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int  # Идентификатор отзыва для сохранённого отзыва в базе данных
