from typing import Type
from sqlalchemy import text, insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from project.infrastructure.postgres.models import Author  # Модель для таблицы Autor
from project.schemas.authorSchema import AuthorSchema, AuthorCreateUpdateSchema
from datetime import date

from pydantic import ValidationError

class AuthorRepository:
    _collection: Type[Author] = Author

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_authorsBooks(
            self,
            session: AsyncSession,
    ) -> list[AuthorSchema]:
        query = select(self._collection)

        authors = await session.scalars(query)

        return [AuthorSchema.model_validate(obj=val) for val in authors.all()]

    async def get_by_id(
            self,
            session: AsyncSession,
            authors_book_id: int
    ) -> AuthorSchema:
        query = select(self._collection).where(self._collection.id_authors_book == authors_book_id)

        result = await session.scalar(query)

        if not result:
            raise AuthorsBookNotFound(_id=authors_book_id)

        return AuthorsBookSchema.model_validate(obj=result)