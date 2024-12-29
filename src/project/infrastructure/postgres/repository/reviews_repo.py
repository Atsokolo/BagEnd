# src/project/infrastructure/postgres/repository/DiscountList_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from datetime import date

from src.project.infrastructure.postgres.models import Reviews
from src.project.schemas.reviewsSchema import ReviewSchema


class ReviewsRepository:
    _collection: Type[Reviews] = Reviews

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_Reviews(
            self,
            session: AsyncSession
    ) -> list[ReviewSchema]:

        query = "SELECT * FROM reviews;"
        result = await session.execute(text(query))

        return [
            ReviewSchema.model_validate(dict(DiscountList))
            for DiscountList in result.mappings().all()
        ]

    async def get_Reviews_by_id(
            self,
            session: AsyncSession,
            id_DiscountList: int
    ) -> ReviewSchema | None:

        query = text("SELECT * FROM reviews WHERE id = :id")
        result = await session.execute(query, {"id": id_DiscountList})

        DiscountList_row = result.mappings().first()

        if DiscountList_row:
            return ReviewSchema.model_validate(dict(DiscountList_row))

        return None

    async def insert_Reviews(
            self,
            session: AsyncSession,
            id: int,
            book_id: str,
            customer_id: int,
            rating: float,
            date: date
    ) -> ReviewSchema | None:

        query = text("""
            INSERT INTO reviews (book_id, customer_id, rating, date) 
            VALUES (:book_id, :customer_id, :rating, :date)
            RETURNING id, book_id, customer_id, rating, date
        """)

        result = await session.execute(query, {
            "book_id": book_id,
            "customer_id": customer_id,
            "rating": rating,
            "date": date
        })

        DiscountList_row = result.mappings().first()

        if DiscountList_row:
            return ReviewSchema.model_validate(dict(DiscountList_row))

        return None

    async def update_Reviews_by_id(
            self,
            session: AsyncSession,
            id: int,
            book_id: str,
            customer_id: int,
            rating: float,
            date: date
    ) -> ReviewSchema | None:

        query = text("""
            UPDATE reviews 
            SET book_id = :book_id, customer_id = :customer_id, rating = :rating, date = :date 
            WHERE id = :id 
            RETURNING id, book_id, customer_id, rating, date
        """)

        result = await session.execute(query, {
            "book_id": book_id,
            "customer_id": customer_id,
            "rating": rating,
            "date": date
        })

        updated_row = result.mappings().first()

        if updated_row:
            return ReviewSchema.model_validate(dict(updated_row))

        return None

    async def delete_Reviews_by_id(
            self,
            session: AsyncSession,
            id: int
    ) -> bool:

        query = text("DELETE FROM reviews WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id})

        deleted_row = result.fetchone()

        return deleted_row is not None
