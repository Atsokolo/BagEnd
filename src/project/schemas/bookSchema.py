from pydantic import BaseModel, ConfigDict


class BookCreateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    autor_id: int  # Может быть не указан при создании
    genre_id: int # Может быть не указан при создании
    cover_type: int # Может быть не указан при создании
    language: str  # Может быть не указан при создании
    publisher_id: int # Может быть не указан при создании


# Схема для книги с идентификатором (для данных из базы)
class BookSchema(BookCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int  # Поле с идентификатором для сохранённых книг

