# src/project/infrastructure/postgres/repository/waiter_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.infrastructure.postgres.models import Genre
from src.project.schemas.genreSchema import GenreSchema


class GenreRepository:
    _collection: Type[Genre] = Genre

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_genres(
            self,
            session: AsyncSession
    ) -> list[GenreSchema]:

        query = "SELECT * FROM genre;"
        result = await session.execute(text(query))

        return [
            GenreSchema.model_validate(dict(genre))
            for genre in result.mappings().all()
        ]

    async def get_genre_by_id(
            self,
            session: AsyncSession,
            id_genre: int
    ) -> GenreSchema | None:

        query = text("SELECT * FROM genre WHERE id = :id;")
        result = await session.execute(query, {"id": id_genre})

        genres_row = result.mappings().first()

        if genres_row:
            return GenreSchema.model_validate(dict(genres_row))

        return None

    async def insert_genre(
            self,
            session: AsyncSession,
            id: int,
            name: str
    ) -> GenreSchema | None:

        query = text("""
            INSERT INTO genre (name) 
            VALUES (:name)
            RETURNING id, name;
        """)

        result = await session.execute(query, {
            "name": name
        })

        genres_row = result.mappings().first()

        if genres_row:
            return GenreSchema.model_validate(dict(genres_row))

        return None

    async def update_genre_by_id(
            self,
            session: AsyncSession,
            id: int,
            name : str
    ) -> GenreSchema | None:

        query = text("""
            UPDATE genre 
            SET name = :name 
            WHERE id = :id 
            RETURNING id, name;
        """)

        result = await session.execute(query, {
            "id": id,
            "name": name
        })

        updated_row = result.mappings().first()

        if updated_row:
            return GenreSchema.model_validate(dict(updated_row))

        return None

    async def delete_genre_by_id(
            self,
            session: AsyncSession,
            id: int
    ) -> bool:

        query = text("DELETE FROM genre WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id})

        deleted_row = result.fetchone()

        return deleted_row is not None
