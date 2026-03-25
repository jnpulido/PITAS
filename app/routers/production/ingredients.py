import datetime
import unittest

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db import get_db
from app.models import Ingredient, IngredientPrice, IngredintStockMoviments
from app.schemes import ingredient
from app.schemes.ingredient import IngredientCreate, IngredientResponse, NewPriceCreate
from sqlalchemy import select
from app.common.enums import MovementType

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredientes"],
)

#para crear ingrediente con su primer precio y cantidad en stock
@router.post(
    "/",
    response_model=IngredientResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ingredient(
    ingredient_data: IngredientCreate,
    db: Session = Depends(get_db)
):
    existing_ingredient = db.scalar(
        select(Ingredient).where(Ingredient.name == ingredient_data.name)
    )

    if existing_ingredient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un ingrediente con ese nombre"
        )

    try:
        new_ingredient = Ingredient(
            name=ingredient_data.name,
            unit=ingredient_data.unit,
            stock=ingredient_data.stock
        )
        db.add(new_ingredient)
        db.flush()

        ingredients_price = IngredientPrice(
            price=ingredient_data.ingredients_price.price ,
            ingredient_id=new_ingredient.id
        )
        db.add(ingredients_price)
        db.flush()


        db.commit()
        db.refresh(new_ingredient)

     
        return new_ingredient


    except Exception as e:
        print(e)
        db.rollback()
        raise


#Agrega un nuevo precio y nueva cantidad en stock
@router.post("/{ingredient_id}/price/", response_model=IngredientResponse)
def create_new_price(ingredient_id:int,new_data:NewPriceCreate, db: Session = Depends(get_db) ):
    ingredient = db.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    ingredient.stock = ingredient.stock + new_data.stock

    new_movement = IngredintStockMoviments(
        type_movement = MovementType.IN,
        quantity= new_data.stock,
        ingredient_id = ingredient.id
    )
    
    new_price = IngredientPrice(
        price= new_data.price,
        ingredient_id = ingredient.id,
    ) 
    db.add(new_movement)
    db.add(new_price)
    db.commit()
    db.refresh(ingredient)
    return ingredient
   




# para mostar todas los ingredientes
@router.get("/",description="muestra todos los ingredientes", response_model=list[IngredientResponse],status_code=201)
async def rad_recipe(db: Session = Depends(get_db)):
    recipes = db.scalars(select(Ingredient)).all()
    return recipes

@router.get("/",description="muestra todos los precios", response_model=list[IngredientResponse],status_code=201)
async def rad_recipe(db: Session = Depends(get_db)):
    recipes = db.scalars(select(Ingredient)).all()
    return recipes
#agregar ingrediente a stock
# @router.post("/create/stock", response_model= IngredientStockResponse)
# def create_ingredient_stock(id, db: Session = Depends(get_db) ):








# #para crear ingrediente
# @router.post(
#     "/",
#     response_model=IngredientResponse,
#     status_code=status.HTTP_201_CREATED
# )
# def create_ingredient(
#     ingredient_data: IngredientCreate,
#     db: Session = Depends(get_db)
# ):
#     existing_ingredient = db.scalar(
#         select(Ingredient).where(Ingredient.name == ingredient_data.name)
#     )

#     if existing_ingredient:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Ya existe un ingrediente con ese nombre"
#         )

#     try:
#         new_ingredient = Ingredient(
#             name=ingredient_data.name,
#             unit=ingredient_data.unit
#         )

#         db.add(new_ingredient)
#         db.flush()

#         price_ingredient = PriceIngredient(
#             date=ingredient_data.price_ingredients.date,
#             quantity=ingredient_data.price_ingredients.quantity,
#             price=ingredient_data.price_ingredients.price,
#             ingredient_id=new_ingredient.id
#         )

#         db.add(price_ingredient)
#         db.commit()
#         db.refresh(new_ingredient)
        
#         new_ingredient = db.scalar(
#             select(Ingredient)
#             .where(Ingredient.id==new_ingredient.id)
#                 .options(joinedload(Ingredient.price_ingredients))
#         )
#         return new_ingredient
        

#     except IntegrityError as e:
#         db.rollback()
#         print(e)
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="No se pudo crear el ingrediente por un problema de integridad de datos"
#         )
#     except Exception as e:
#         print(e)
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Ocurrió un error al crear el ingrediente"
#         )




        # a = db.execute(
        #     select(Ingredient.id, Ingredient.name, Ingredient.unit, PriceIngredient.price, IngredientStock.quantity)
        #     .select_from(Ingredient)
        #     .join(PriceIngredient, PriceIngredient.ingredient_id==new_ingredient.id)
        #     .join(IngredientStock, IngredientStock.ingredient_id == new_ingredient.id)
        #     .where(Ingredient.id==new_ingredient.id)
        #     .order_by(PriceIngredient.date.desc())
        #     .limit(1)
        # ).all()
        # print(a[0]._mapping)
        # a = IngredientResponseComplete.model_validate(a[0]._mapping)
        # # print(a[0]._mapping)
        # return a




        # ingredient_stock = db.scalar(
        #     select(IngredientStock)
        #     .where(IngredientStock.ingredient_id == new_ingredient.id)
        #     .options(
        #         joinedload(IngredientStock.ingredient).joinedload( Ingredient.price_ingredients )
                   
               
        #     )
        # )
        # print("los datos son",ingredient_stock),

        # return ingredient_stock