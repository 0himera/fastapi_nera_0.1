from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import db_helper, Product
from core.schemas.product import ProductCreate, ProductRead, ProductUpdate
from core.config import settings
from core.crud.product import create_product, get_products, get_product, delete_product, update_product

router = APIRouter(
    prefix=settings.api.v1.products,
    tags=["Products"],
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_helper.session_getter():
        yield session


@router.post("", response_model=ProductRead)
async def product_create(
    product_data: ProductCreate, session: AsyncSession = Depends(get_async_db)
):
    product = await create_product(product_data=product_data, db=session)

    # Загружаем связанные изображения
    result = await session.execute(
        select(Product).options(selectinload(Product.images)).where(Product.id == product.id)
    )
    product_with_images = result.scalar_one()

    return product_with_images


@router.get("/{product_id}", response_model=ProductRead)
async def product_get(product_id: int, session: AsyncSession = Depends(get_async_db)):
    product_ = await get_product(db=session, product_id=product_id)
    if product_ is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_


@router.get("", response_model=list[ProductRead])
async def products_get(
    skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_db),
):
    return await get_products(skip=skip, limit=limit, db=session)


@router.put("/{product_id}", response_model=ProductRead)
async def product_update(
    product_id: int,
    product_data: ProductUpdate,
    session: AsyncSession = Depends(get_async_db),
):
    product_ = await get_product(db=session, product_id=product_id)
    if product_ is None:
        raise HTTPException(status_code=404, detail="Product not found")

    updated_product = await update_product(db=session, product_id=product_id, product_data=product_data)

    return updated_product


@router.delete("/{product_id}", response_model=ProductRead)
async def product_delete(product_id: int, session: AsyncSession = Depends(get_async_db)):
    product_ = await delete_product(db=session, product_id=product_id)
    if product_ is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_
