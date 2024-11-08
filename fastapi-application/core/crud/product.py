from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from core.models.product import Product, Image
from core.schemas.product import ProductCreate, ProductUpdate


# Асинхронная функция для создания продукта
async def create_product(db: AsyncSession, product_data: ProductCreate):
    try:
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price
        )
        db.add(product)
        await db.commit()
        await db.refresh(product)

        # Создаем связанные изображения
        if product_data.images:
            for image_data in product_data.images:
                image = Image(url=image_data.url, product_id=product.id)
                db.add(image)
            await db.commit()

        # Обновляем продукт с новыми изображениями
        await db.refresh(product)
        return product

    except Exception as e:
        await db.rollback()  # Откатываем транзакцию при ошибке
        raise e


# Асинхронная функция для получения продукта по ID
async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).options(selectinload(Product.images)).where(Product.id == product_id))
    return result.scalars().first()


# Асинхронная функция для получения всех продуктов
async def get_products(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.images))  # Загрузит связанные images асинхронно
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


# Асинхронная функция для обновления продукта
async def update_product(db: AsyncSession, product_id: int, product_data: ProductUpdate):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()

    if not product:
        return None  # Если продукт не найден

    # Обновляем поля продукта
    if product_data.name is not None:
        product.name = product_data.name
    if product_data.description is not None:
        product.description = product_data.description
    if product_data.price is not None:
        product.price = product_data.price

    # Обновляем изображения, если они есть
    if product_data.images:
        await db.execute(delete(Image).where(Image.product_id == product.id))
        await db.commit()
        for image_data in product_data.images:
            new_image = Image(url=image_data.url, product_id=product.id)
            db.add(new_image)

    await db.commit()
    await db.refresh(product)  # Обновляем объект после коммита
    return product


# Асинхронная функция для удаления продукта
async def delete_product(db: AsyncSession, product_id: int):
    # Получаем продукт по ID
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()

    # Если продукт существует, удаляем его
    if product:
        # Удаляем изображения, если это необходимо
        await db.execute(delete(Image).where(Image.product_id == product.id))

        # Удаляем сам продукт
        await db.delete(product)
        await db.commit()
    return product

