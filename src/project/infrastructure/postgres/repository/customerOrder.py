# src/project/infrastructure/postgres/repository/DiscountList_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.infrastructure.postgres.models import CustomerOrder
from src.project.schemas.publisherSchema import PublisherSchema


class PublisherRepository:
    _collection: Type[CustomerOrder] = CustomerOrder

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_Publisher(
            self,
            session: AsyncSession
    ) -> list[PublisherSchema]:

        query = "SELECT * FROM publisherSchema;"
        result = await session.execute(text(query))

        return [
            PublisherSchema.model_validate(dict(DiscountList))
            for DiscountList in result.mappings().all()
        ]

    async def get_Publisher_by_id(
            self,
            session: AsyncSession,
            id_DiscountList: int
    ) -> PublisherSchema | None:

        query = text("SELECT * FROM publisher WHERE id = :id")
        result = await session.execute(query, {"id": id_DiscountList})

        DiscountList_row = result.mappings().first()

        if DiscountList_row:
            return PublisherSchema.model_validate(dict(DiscountList_row))

        return None

    async def insert_Publisher(
            self,
            session: AsyncSession,
            id: int,
            name: str,
            salary: int,
            rating: float,
            status: str
    ) -> PublisherSchema | None:

        query = text("""
            INSERT INTO publisher (name, salary, rating, status) 
            VALUES (:name, :salary, :rating, :status)
            RETURNING id, name, salary, rating, status
        """)

        result = await session.execute(query, {
            "name": name,
            "salary": salary,
            "rating": rating,
            "status": status
        })

        DiscountList_row = result.mappings().first()

        if DiscountList_row:
            return PublisherSchema.model_validate(dict(DiscountList_row))

        return None

    async def update_Publisher_by_id(
            self,
            session: AsyncSession,
            id_DiscountList: int,
            name: str,
            salary: int,
            rating: float,
            status: str
    ) -> PublisherSchema | None:

        query = text("""
            UPDATE publisher 
            SET name = :name, salary = :salary, rating = :rating, status = :status 
            WHERE id = :id 
            RETURNING id, name, salary, rating, status
        """)

        result = await session.execute(query, {
            "id": id_DiscountList,
            "name": name,
            "salary": salary,
            "rating": rating,
            "status": status
        })

        updated_row = result.mappings().first()

        if updated_row:
            return PublisherSchema.model_validate(dict(updated_row))

        return None

    async def delete_Publisher_by_id(
            self,
            session: AsyncSession,
            id_DiscountList: int
    ) -> bool:

        query = text("DELETE FROM publisher WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_DiscountList})

        deleted_row = result.fetchone()

        return deleted_row is not None
