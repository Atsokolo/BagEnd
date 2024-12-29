# src/project/infrastructure/postgres/repository/waiter_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, decimal

from src.project.infrastructure.postgres.models import OrderDetails
from src.project.schemas.orderDetailSchema import OrderDetailsSchema


class OrderDetailsRepository:
    _collection: Type[OrderDetails] = OrderDetails

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
    ) -> list[OrderDetailsSchema]:

        query = "SELECT * FROM order_details;"
        result = await session.execute(text(query))

        return [
            OrderDetailsSchema.model_validate(dict(genre))
            for genre in result.mappings().all()
        ]

    async def get_genre_by_id(
            self,
            session: AsyncSession,
            id_genre: int
    ) -> OrderDetailsSchema | None:

        query = text("SELECT * FROM order_details WHERE id = :id;")
        result = await session.execute(query, {"id": id_genre})

        first= result.mappings().first()

        if first:
            return OrderDetailsSchema.model_validate(dict(first))

        return None

    async def insert_order_detales(
            self,
            session: AsyncSession,
            id: int,
            order_id: int,
            book_id: int,
            count: int,
            price_per_unit: decimal
    ) ->OrderDetailsSchema | None:

        query = text("""
            INSERT INTO order_details (order_id, book_id, count, price_per_unit) 
            VALUES (:order_id, :book_id, :count, :price_per_unit)
            RETURNING id, order_id, book_id, count, price_per_unit;
        """)

        result = await session.execute(query, {
            "order_id": order_id,
            "book_id": book_id,
            "count": count,
            "price_per_unit": price_per_unit
        })

        genres_row = result.mappings().first()

        if genres_row:
            return OrderDetailsSchema.model_validate(dict(genres_row))

        return None

    async def update_order_details_by_id(
            self,
            session: AsyncSession,
            id: int,
            order_id: int,
            book_id: int,
            count: int,
            price_per_unit: decimal
    ) -> OrderDetailsSchema | None:

        query = text("""
            UPDATE order_details 
            SET order_id = :order_id, book_id = :book_id, count = :count, price_per_unit = :price_per_unit
            WHERE id = :id 
            RETURNING id, order_id, book_id, count, price_per_unit;
        """)

        result = await session.execute(query, {
            "id": id,
            "order_id": order_id,
            "book_id": book_id,
            "count": count,
            "price_per_unit": price_per_unit
        })

        updated_row = result.mappings().first()

        if updated_row:
            return OrderDetailsSchema.model_validate(dict(updated_row))

        return None

    async def delete_order_details_by_id(
            self,
            session: AsyncSession,
            id: int
    ) -> bool:

        query = text("DELETE FROM order_details WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id})

        deleted_row = result.fetchone()

        return deleted_row is not None
