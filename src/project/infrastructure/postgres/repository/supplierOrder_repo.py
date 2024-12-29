# src/project/infrastructure/postgres/repository/waiter_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, decimal, datetime, date

from src.project.infrastructure.postgres.models import SupplierOrder
from src.project.schemas.supplierOrderSchema import SupplierOrderSchema


class SupplierOrderRepository:
    _collection: Type[SupplierOrder] = SupplierOrder

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_supplier_order(
            self,
            session: AsyncSession
    ) -> list[SupplierOrderSchema]:

        query = "SELECT * FROM supplier_order;"
        result = await session.execute(text(query))

        return [
            SupplierOrderSchema.model_validate(dict(genre))
            for genre in result.mappings().all()
        ]

    async def get_supplier_order_by_id(
            self,
            session: AsyncSession,
            id_genre: int
    ) -> SupplierOrderSchema | None:

        query = text("SELECT * FROM supplier_order WHERE id = :id;")
        result = await session.execute(query, {"id": id_genre})

        first= result.mappings().first()

        if first:
            return SupplierOrderSchema.model_validate(dict(first))

        return None

    async def insert_supplier_order_detales(
            self,
            session: AsyncSession,
            id: int,
            supplier_id: int,
            order_date: date,
            total: int,
            status: int

    ) ->SupplierOrderSchema | None:

        query = text("""
            INSERT INTO supplier_order (supplier_id, order_date, total, status) 
            VALUES (:supplier_id, :order_date, :total, :status)
            RETURNING id, supplier_id, order_date, total, status;
        """)

        result = await session.execute(query, {
            "supplier_id": supplier_id,
            "order_date": order_date,
            "total": total,
            "status": status
        })

        genres_row = result.mappings().first()

        if genres_row:
            return SupplierOrderSchema.model_validate(dict(genres_row))

        return None

    async def update_supplier_order_by_id(
            self,
            session: AsyncSession,
            id: int,
            supplier_id: int,
            order_date: date,
            total: int,
            status: int
    ) -> SupplierOrderSchema | None:

        query = text("""
            UPDATE supplier_order
            SET supplier_id = :supplier_id, order_date = :order_date, total = :total, status = :status
            WHERE id = :id 
            RETURNING id, supplier_id, order_date, total, status;
        """)

        result = await session.execute(query, {
            "id": id,
            "supplier_id": supplier_id,
            "order_date": order_date,
            "total": total,
            "status": status
        })

        updated_row = result.mappings().first()

        if updated_row:
            return SupplierOrderSchema.model_validate(dict(updated_row))

        return None

    async def delete_supplier_order_by_id(
            self,
            session: AsyncSession,
            id: int
    ) -> bool:

        query = text("DELETE FROM supplier_order WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id})

        deleted_row = result.fetchone()

        return deleted_row is not None
