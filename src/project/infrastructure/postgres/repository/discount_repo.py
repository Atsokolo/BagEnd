# src/project/infrastructure/postgres/repository/Discount_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import text, insert, update, delete, select
from datetime import date

from src.project.infrastructure.postgres.models import Discount
from src.project.schemas.discountSchema import DiscountSchema


class DiscountRepository:
    _collection: Type[Discount] = Discount

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_Discounts(
            self,
            session: AsyncSession
    ) -> list[DiscountSchema]:

        query = "SELECT * FROM discount;"
        result = await session.execute(text(query))

        return [
            DiscountSchema.model_validate(dict(Discount))
            for Discount in result.mappings().all()
        ]

    async def get_Discount_by_id(
            self,
            session: AsyncSession,
            id_Discount: int
    ) -> DiscountSchema | None:

        query = text("SELECT * FROM discount WHERE id = :id")
        result = await session.execute(query, {"id": id_Discount})

        Discount_row = result.mappings().first()

        if Discount_row:
            return DiscountSchema.model_validate(dict(Discount_row))

        return None

    async def insert_Discount(
            self,
            session: AsyncSession,
            id: int,
            percent: int,
            start_date: date,
            end_date: date,
    ) -> DiscountSchema | None:

        query = text("""
            INSERT INTO discount (percent, start_date, end_date) 
            VALUES (:percent, :start_date, :end_date)
            RETURNING id, percent, start_date, end_date
        """)

        result = await session.execute(query, {
            "percent": percent,
            "start_date": start_date,
            "end_date": end_date,
        })

        Discount_row = result.mappings().first()

        if Discount_row:
            return DiscountSchema.model_validate(dict(Discount_row))

        return None

    async def update_Discount_by_id(
            self,
            session: AsyncSession,
            id: int,
            percent: int,
            start_date: date,
            end_date: date,
    ) -> DiscountSchema | None:

        query = text("""
            UPDATE discount 
            percent, start_date, end_date
            SET percent = :percent, start_date = :start_date, end_date = :end_date
            WHERE id = :id 
            RETURNING id, percent, start_date, end_date
        """)

        result = await session.execute(query, {
            "id": id,
            "percent": percent,
            "start_date": start_date,
            "end_date": end_date
        })

        updated_row = result.mappings().first()

        if updated_row:
            return DiscountSchema.model_validate(dict(updated_row))

        return None

    async def delete_Discount_by_id(
            self,
            session: AsyncSession,
            id_Discount: int
    ) -> bool:

        query = text("DELETE FROM discount WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_Discount})

        deleted_row = result.fetchone()

        return deleted_row is not None
