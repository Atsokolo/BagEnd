# src/project/infrastructure/postgres/repository/CoverType_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.infrastructure.postgres.models import CoverType
from src.project.schemas.coverTypeSchema import CoverTypeSchema


class CoverTypeRepository:
    _collection: Type[CoverType] = CoverType

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_CoverTypes(
            self,
            session: AsyncSession
    ) -> list[CoverTypeSchema]:

        query = "SELECT * FROM CoverType;"
        result = await session.execute(text(query))

        return [
            CoverTypeSchema.model_validate(dict(CoverType))
            for CoverType in result.mappings().all()
        ]

    async def get_CoverType_by_id(
            self,
            session: AsyncSession,
            id_CoverType: int
    ) -> CoverTypeSchema | None:

        query = text("SELECT * FROM CoverType WHERE id = :id")
        result = await session.execute(query, {"id": id_CoverType})

        CoverType_row = result.mappings().first()

        if CoverType_row:
            return CoverTypeSchema.model_validate(dict(CoverType_row))

        return None

    async def insert_CoverType(
            self,
            session: AsyncSession,
            id: int,
            name: str
    ) -> CoverTypeSchema | None:

        query = text("""
            INSERT INTO CoverType (name) 
            VALUES (:name)
            RETURNING id, name
        """)

        result = await session.execute(query, {
            "name": name
        })

        CoverType_row = result.mappings().first()

        if CoverType_row:
            return CoverTypeSchema.model_validate(dict(CoverType_row))

        return None

    async def update_CoverType_by_id(
            self,
            session: AsyncSession,
            id_CoverType: int,
            name: str,
    ) -> CoverTypeSchema | None:

        query = text("""
            UPDATE CoverType 
            SET name = :name
            WHERE id = :id 
            RETURNING id, name
        """)

        result = await session.execute(query, {
            "id": id_CoverType,
            "name": name
        })

        updated_row = result.mappings().first()

        if updated_row:
            return CoverTypeSchema.model_validate(dict(updated_row))

        return None

    async def delete_CoverType_by_id(
            self,
            session: AsyncSession,
            id_CoverType: int
    ) -> bool:

        query = text("DELETE FROM CoverType WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_CoverType})

        deleted_row = result.fetchone()

        return deleted_row is not None
