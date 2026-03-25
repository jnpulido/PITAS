from __future__ import annotations
from typing import List
from decimal import Decimal
from sqlalchemy import ForeignKey, String, Float, Numeric
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import DateTime, func
from sqlalchemy import Enum as SQLEnum
from app.common.enums import MovementType


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

    recipe: Mapped["Recipe"] = relationship(back_populates="recipe_ingredients")
    ingredient: Mapped[list["Ingredient"]] = relationship(back_populates="recipe_ingredients")

class Batch(Base):
    __tablename__ = "batches"
    id:Mapped[int] = mapped_column(primary_key=True , index=True)
    start_date : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    end_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True
    )
    planned_quantity:Mapped[int] = mapped_column(nullable=False)
    produced_quantity:Mapped[int] = mapped_column(nullable=True)
    recipe_id:  Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
)
    recipe: Mapped["Recipe"] =relationship(back_populates="batch")



class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    quantity_base:Mapped[int] = mapped_column(nullable=True)
    stock_units:Mapped[int] = mapped_column(nullable=False)

    recipe_ingredients: Mapped[List["RecipeIngredient"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan"
    ) 
    batch : Mapped[list[Batch]] =relationship(back_populates="recipe")

#✅
class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)
    stock:Mapped[int] = mapped_column(nullable=True)
    ingredients_price: Mapped[list["IngredientPrice"]] = relationship(
        back_populates="ingredient",
        
    ) 
    moviments_ingredients: Mapped[List["IngredintStockMoviments"]] = relationship(
        back_populates="ingredient",
    
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    recipe_ingredients: Mapped[List["RecipeIngredient"]] = relationship(
        back_populates="ingredient"
    )
   
   


#✅
class IngredientPrice(Base):
    __tablename__ = "ingredients_price"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="ingredients_price"
    )



    
# despues ahgo la tabla de movimientos
class IngredintStockMoviments(Base):
    __tablename__= "ingredients_stock_moviments"
    id:Mapped[int]= mapped_column(primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    type_movement: Mapped[MovementType] = mapped_column(
    SQLEnum(MovementType, name="movement_type"),
    nullable=True
)
    quantity:Mapped[int] = mapped_column(nullable=False)
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="moviments_ingredients"
    )




    ######### para entender"#######
# class CompanyUserRole(Base):
#     __tablename__ = 'company_user_role'
#     user_id: Mapped[int] = mapped_column(
#         ForeignKey('company_user.id'), primary_key=True)
#     role_id: Mapped[int] = mapped_column(
#         ForeignKey('role.id'), primary_key=True)
#     start_date: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), primary_key=True, server_default=func.now())
#     end_date: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), nullable=True)
#     __table_args__ = (
#         UniqueConstraint('user_id', 'role_id', 'start_date',
#                          'end_date', name='unique_user_role_dates'),
#     )



# class RolePermission(Base):
#     __tablename__ = 'role_permission'
#     role_id: Mapped[int] = mapped_column(
#         ForeignKey('role.id'), primary_key=True)
#     permission_id: Mapped[int] = mapped_column(
#         ForeignKey('permission.id'), primary_key=True)




#     class CompanyUser(Base):
#     __tablename__ = 'company_user'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     identification: Mapped[str] = mapped_column(
#         String(255), unique=True, nullable=False)
#     first_name: Mapped[str] = mapped_column(String(255))
#     last_name: Mapped[str] = mapped_column(String(255))
#     email: Mapped[str] = mapped_column(
#         String(255), unique=True, nullable=False)
#     active: Mapped[bool] = mapped_column(Boolean, default=True)
#     is_superuser: Mapped[bool] = mapped_column(
#         Boolean, nullable=False, default=False, server_default=text("false")
#     )

#     roles = relationship(
#         "Role",
#         secondary=CompanyUserRole.__table__,
#         back_populates="users"
#     )
    
#     work_orders = relationship(
#         "WorkOrder",
#         secondary=CompanyUserWorkOrder.__table__,
#         back_populates="users"
#     )


    
#     class Role(Base):
#     __tablename__ = 'role'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
#     description: Mapped[str] = mapped_column(String(255))
#     sector_id: Mapped[int] = mapped_column(ForeignKey('sector.id'), nullable=False)
    
#     sector: Mapped["Sector"] = relationship("Sector", back_populates="roles")

#     users = relationship(
#         "CompanyUser",
#         secondary=CompanyUserRole.__table__,
#         back_populates="roles"
#     )

#     permissions = relationship(
#         "Permission",
#         secondary=RolePermission.__table__,
#         back_populates="roles"
#     )



#     class Permission(Base):
#     __tablename__ = 'permission'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     code: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
#     description: Mapped[str] = mapped_column(String(255))

#     roles = relationship(
#         "Role",
#         secondary=RolePermission.__table__,
#         back_populates="permissions"
#     )
