from typing import Type
from sqlalchemy import text, insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import date

from project.infrastructure.postgres.models import Author  # Модель для таблицы Autor
from project.schemas.authorSchema import AuthorSchema, AuthorCreateUpdateSchema


class AuthorRepository:
    _collection: Type[Author] = Author

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_authors(
            self,
            session: AsyncSession,
    ) -> list[AuthorSchema]:
        query = select(self._collection)

        query = "SELECT * FROM author;"
        result = await session.execute(text(query))

        return [
            AuthorSchema.model_validate(dict(author))
            for author in result.mappings().all()
        ]

    async def get_by_id(
            self,
            session: AsyncSession,
            id_author: int
    ) -> AuthorSchema:
        query = text("SELECT * FROM author WHERE id = :id")
        result = await session.execute(query, {"id": id_author})

        author_row = result.mappings().first()

        if author_row:
            return AuthorSchema.model_validate(dict(author_row))

        return None

    async def insert_author(
            self,
            session: AsyncSession,
            id: int,
            name: str,
            date_of_birth: date,
    ) -> AuthorSchema | None:

        query = text("""
            INSERT INTO author (name, date_of_birth) 
            VALUES (:name, :date_of_birth)
            RETURNING id, name, date_of_birth
        """)

        result = await session.execute(query, {
            "name": name,
            "date_of_birth": date_of_birth
        })

        author_row = result.mappings().first()

        if author_row:
            return AuthorSchema.model_validate(dict(author_row))

        return None

    async def update_author_by_id(
            self,
            session: AsyncSession,
            id: int,
            name: str,
            date_of_birth: date
    ) -> AuthorSchema | None:

        query = text("""
            UPDATE author 
            SET name = :name, date_of_birth = :date_of_birth
            WHERE id = :id 
            RETURNING id, name, date_of_birth
        """)

        result = await session.execute(query, {
            "id": id,
            "name": name,
            "date_of_birth": date_of_birth
        })

        updated_row = result.mappings().first()

        if updated_row:
            return AuthorSchema.model_validate(dict(updated_row))

        return None

    async def delete_author_by_id(
            self,
            session: AsyncSession,
            id: int
    ) -> bool:

        query = text("DELETE FROM author WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id})

        deleted_row = result.fetchone()

        return deleted_row is not None