from typing import List, Optional
from pydantic import BaseModel, ConfigDict


# Pydantic модель для Image
class ImageRead(BaseModel):
    id: int
    url: str

    model_config = ConfigDict(from_attributes=True)


class ImageCreate(BaseModel):
    url: str


# Базовая модель для продуктов
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: int


# Модель для создания продукта
class ProductCreate(ProductBase):
    images: Optional[List[ImageCreate]] = None  # Можно добавить изображения при создании продукта


# Модель для обновления продукта
class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    images: Optional[List[ImageCreate]] = None


# Модель для чтения данных продукта, включая изображения
class ProductRead(ProductBase):
    id: int
    images: List[ImageRead] = []  # Включаем связанные изображения

    model_config = ConfigDict(from_attributes=True)