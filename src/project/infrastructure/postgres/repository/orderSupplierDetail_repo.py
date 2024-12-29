# src/project/infrastructure/postgres/repository/DiscountList_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.infrastructure.postgres.models import OrderSupplierDetails
from src.project.schemas.orderSupplierDetailSchema import OrderSupplierDetailsSchema


class OrderSupplierDetailsRepository:
    _collection: Type[OrderSupplierDetails] = OrderSupplierDetails

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_order_supplier_details_schema(
            self,
            session: AsyncSession
    ) -> list[OrderSupplierDetailsSchema]:

        query = "SELECT * FROM order_supplier_details;"
        result = await session.execute(text(query))

        return [
            OrderSupplierDetailsSchema.model_validate(dict(DiscountList))
            for DiscountList in result.mappings().all()
        ]

    async def get_order_supplier_details_schema_by_id(
            self,
            session: AsyncSession,
            id_DiscountList: int
    ) -> OrderSupplierDetailsSchema | None:

        query = text("SELECT * FROM order_supplier_details WHERE id = :id;")
        result = await session.execute(query, {"id": id_DiscountList})

        DiscountList_row = result.mappings().first()

        if DiscountList_row:
            return OrderSupplierDetailsSchema.model_validate(dict(DiscountList_row))

        return None

    async def insert_order_supplier_details_schema(
            self,
            session: AsyncSession,
            id: int,
            order_publ_id: int,
            book_id: int,
            count: int,
            price_per_unit: int
    ) -> OrderSupplierDetailsSchema | None:

        query = text("""
            INSERT INTO order_supplier_details (order_publ_id, book_id, count, price_per_unit) 
            VALUES (:order_publ_id, :book_id, :count, :price_per_unit)
            RETURNING id, order_publ_id, book_id, count, price_per_unit;
        """)

        result = await session.execute(query, {
            "order_publ_id": order_publ_id,
            "salary": book_id,
            "rating": count,
            "price_per_unit": price_per_unit
        })

        DiscountList_row = result.mappings().first()

        if DiscountList_row:
            return OrderSupplierDetailsSchema.model_validate(dict(DiscountList_row))

        return None

    async def update_order_supplier_details_schema_by_id(
            self,
            session: AsyncSession,
            id: int,
            order_publ_id: int,
            book_id: int,
            count: int,
            price_per_unit: int
    ) -> OrderSupplierDetailsSchema | None:

        query = text("""
            UPDATE order_supplier_details 
            SET order_publ_id = :order_publ_id, book_id = :book_id, count = :count, price_per_unit = :price_per_unit
            WHERE id = :id 
            RETURNING id, order_publ_id, book_id, count, price_per_unit;
        """)

        result = await session.execute(query, {
            "id": id,
            "order_publ_id": order_publ_id,
            "salary": book_id,
            "rating": count,
            "price_per_unit": price_per_unit
        })

        updated_row = result.mappings().first()

        if updated_row:
            return OrderSupplierDetailsSchema.model_validate(dict(updated_row))

        return None

    async def delete_order_supplier_details_schema_by_id(
            self,
            session: AsyncSession,
            id_DiscountList: int
    ) -> bool:

        query = text("DELETE FROM order_supplier_details WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_DiscountList})

        deleted_row = result.fetchone()

        return deleted_row is not None
