from __future__ import annotations
from typing import List
from decimal import Decimal
from sqlalchemy import Boolean, ForeignKey, String, Float, Numeric
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import DateTime, func
from sqlalchemy import Enum as SQLEnum
from app.common.enums import (
    MovementType,
    MovementTypeCost,
    movement_type_enum,
    movement_type_cost_enum,
)


class Base(DeclarativeBase):
    pass



class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"),
        primary_key=True
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        primary_key=True
    )
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)

    recipe: Mapped["Recipe"] = relationship(back_populates="recipe_ingredients")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="recipe_ingredients")


class BatchCost(Base):
    __tablename__ = "batch_costs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    batch_id: Mapped[int] = mapped_column(ForeignKey("batches.id", ondelete="CASCADE"), nullable=False)
    type_movement: Mapped[MovementTypeCost] = mapped_column(
        SQLEnum(MovementTypeCost, name="movement_type_cost"),
        nullable=False
    )
    concept: Mapped[str] = mapped_column(String(120), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    batch: Mapped["Batch"] = relationship(back_populates="batch_costs")


class Batch(Base):
    __tablename__ = "batches"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    planned_quantity: Mapped[int] = mapped_column(nullable=False)
    produced_quantity: Mapped[int | None] = mapped_column(nullable=True)

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    recipe: Mapped["Recipe"] = relationship(back_populates="batches")
    batch_costs: Mapped[list["BatchCost"]] = relationship(
        back_populates="batch",
        cascade="all, delete-orphan"
    )


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    quantity_base: Mapped[int | None] = mapped_column(nullable=True)
    stock_units: Mapped[int] = mapped_column(nullable=False)

    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan"
    )
    batches: Mapped[list["Batch"]] = relationship(back_populates="recipe")
    product: Mapped["Product"] = relationship(back_populates="recipe", uselist=False)


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)

    ingredient_prices: Mapped[list["IngredientPrice"]] = relationship(
        back_populates="ingredient",
        cascade="all, delete-orphan"
    )
    stock_movements: Mapped[list["IngredientStockMovement"]] = relationship(
        back_populates="ingredient",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="ingredient"
    )


class IngredientPrice(Base):
    __tablename__ = "ingredient_prices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    ingredient: Mapped["Ingredient"] = relationship(back_populates="ingredient_prices")


class IngredientStockMovement(Base):
    __tablename__ = "ingredient_stock_movements"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    type_movement: Mapped[MovementType] = mapped_column(
        movement_type_enum,
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(nullable=False)
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    ingredient: Mapped["Ingredient"] = relationship(back_populates="stock_movements")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    stock: Mapped[int | None] = mapped_column(nullable=True)
    validity: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    recipe: Mapped["Recipe"] = relationship(back_populates="product")
    presentations: Mapped[list["Presentation"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )
    stock_movements: Mapped[list["ProductStockMovement"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )


class ProductStockMovement(Base):
    __tablename__ = "product_stock_movements"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    type_movement: Mapped[MovementType] = mapped_column(
        movement_type_enum,
        nullable=False
    )
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(nullable=False)

    product: Mapped["Product"] = relationship(back_populates="stock_movements")


class Presentation(Base):
    __tablename__ = "presentations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    unit_quantity: Mapped[int | None] = mapped_column(nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    validity: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    product: Mapped["Product"] = relationship(back_populates="presentations")
    price_history: Mapped[list["PresentationPriceHistory"]] = relationship(
        back_populates="presentation",
        cascade="all, delete-orphan"
    )
    order_details: Mapped[list["OrderDetail"]] = relationship(back_populates="presentation")


class PresentationPriceHistory(Base):
    __tablename__ = "presentation_price_history"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    presentation_id: Mapped[int] = mapped_column(
        ForeignKey("presentations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    presentation: Mapped["Presentation"] = relationship(back_populates="price_history")


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(120), nullable=False)
    address: Mapped[str] = mapped_column(String(120), nullable=False)

    orders: Mapped[list["Order"]] = relationship(back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    customer: Mapped["Customer"] = relationship(back_populates="orders")
    order_details: Mapped[list["OrderDetail"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderDetail(Base):
    __tablename__ = "order_details"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    presentation_id: Mapped[int] = mapped_column(
        ForeignKey("presentations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    quantity: Mapped[int] = mapped_column(nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    order: Mapped["Order"] = relationship(back_populates="order_details")
    presentation: Mapped["Presentation"] = relationship(back_populates="order_details")