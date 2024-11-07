from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from core.models.product import Product, Image
from core.schemas.product import ProductCreate, ProductUpdate, ImageCreate


# Асинхронная функция для создания продукта
async def create_product(db: AsyncSession, product_data: ProductCreate):
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

    return product


# Асинхронная функция для получения продукта по ID
async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalars().first()


# Асинхронная функция для получения всех продуктов
async def get_products(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()


# Асинхронная функция для обновления продукта
async def update_product(db: AsyncSession, product: Product, product_data: ProductUpdate):
    if product_data.name:
        product.name = product_data.name
    if product_data.description:
        product.description = product_data.description
    if product_data.price:
        product.price = product_data.price
    await db.commit()

    # Обновляем изображения
    if product_data.images:
        await db.execute(select(Image).where(Image.product_id == product.id).delete())
        for image_data in product_data.images:
            image = Image(url=image_data.url, product_id=product.id)
            db.add(image)
        await db.commit()

    await db.refresh(product)
    return product


# Асинхронная функция для удаления продукта
async def delete_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if product:
        await db.delete(product)
        await db.commit()
    return product
