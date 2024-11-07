from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class Product(Base, IntIdPkMixin):

    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[int]
    images: Mapped[List["Image"]] = relationship(
        "Image",
        back_populates="product",
        cascade="all, delete-orphan",
    )


class Image(Base, IntIdPkMixin):

    url: Mapped[str] = mapped_column(String(255))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship(back_populates="images")
