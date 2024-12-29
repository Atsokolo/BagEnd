# src/project/infrastructure/postgres/repository/DiscountList_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.infrastructure.postgres.models import DiscountList
from src.project.schemas.discountListSchema import DiscountListSchema


class DiscountListRepository:
    _collection: Type[DiscountList] = DiscountList

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_DiscountLists(
            self,
            session: AsyncSession
    ) -> list[DiscountListSchema]:

        query = "SELECT * FROM discountList;"
        result = await session.execute(text(query))

        return [
            DiscountListSchema.model_validate(dict(DiscountList))
            for DiscountList in result.mappings().all()
        ]

    async def get_DiscountList_by_id(
            self,
            session: AsyncSession,
            id_DiscountList: int
    ) -> DiscountListSchema | None:

        query = text("SELECT * FROM discountList WHERE id = :id")
        result = await session.execute(query, {"id": id_DiscountList})

        DiscountList_row = result.mappings().first()

        if DiscountList_row:
            return DiscountListSchema.model_validate(dict(DiscountList_row))

        return None

    async def insert_DiscountList(
            self,
            session: AsyncSession,
            id: int,
            book_id: str,
            discount_id: int
    ) -> DiscountListSchema | None:

        query = text("""
            INSERT INTO discountList (book_id, discount_id) 
            VALUES ( :book_id, :discount_id)
            RETURNING id, book_id, discount_id
        """)

        result = await session.execute(query, {
            "book_id": book_id,
            "discount_id": discount_id,
        })

        DiscountList_row = result.mappings().first()

        if DiscountList_row:
            return DiscountListSchema.model_validate(dict(DiscountList_row))

        return None

    async def update_DiscountList_by_id(
            self,
            session: AsyncSession,
            id: int,
            book_id: str,
            discount_id: int
    ) -> DiscountListSchema | None:

        query = text("""
            UPDATE discountList 
            SET book_id = :book_id, discount_id = :discount_id
            WHERE id = :id 
            RETURNING id, book_id, discount_id
        """)

        result = await session.execute(query, {
            "id": id,
            "book_id": book_id,
            "discount_id": discount_id,
        })

        updated_row = result.mappings().first()

        if updated_row:
            return DiscountListSchema.model_validate(dict(updated_row))

        return None

    async def delete_DiscountList_by_id(
            self,
            session: AsyncSession,
            id_DiscountList: int
    ) -> bool:

        query = text("DELETE FROM discountList WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_DiscountList})

        deleted_row = result.fetchone()

        return deleted_row is not None
