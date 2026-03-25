from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Select, select
from sqlalchemy.orm import Session, joinedload
from app.models import Batch, Ingredient, IngredintStockMoviments

from app.common.ingredients_requirements import ingredients_requirements, validate_ingredient_stock
from app.db import get_db
from app.schemes.batches import BatchesCompleted
from app.common.enums import MovementType


router = APIRouter(
    prefix="/batches",
)

# calular la cantidad de ingredientes de acuerdo a la cantidad de unidades
@router.get("/{recipe_id}")
def calcule_ingredients(recipe_id:int, planned_quantity:int, db:Session = Depends(get_db)):
    return ingredients_requirements(recipe_id,planned_quantity, db)


#calcula cantidades y valida  stock
@router.post("/create")
def create_batch(recipe_id:int, planned_quantity:int, db:Session = Depends(get_db)):
     requirements = ingredients_requirements(recipe_id, planned_quantity, db) 
     validate_ingredient_stock(requirements) 
     new_batch = Batch(
          planned_quantity = planned_quantity,
          recipe_id = recipe_id
     )
     db.flush()
     # actualizar el stock cuando ya se producen las arepas
     for req in requirements:
        ingredient = db.scalar(
            select(Ingredient).where(Ingredient.id == req["id"])
        )

        if not ingredient:
            raise HTTPException(status_code=404, detail=f"Ingredient {req['id']} not found")

        ingredient.stock -= req["quantity"]
        #registrar el movimiento de salida de los ingredientes
        new_movement= IngredintStockMoviments(
            ingredient_id=req["id"],
            type_movement= MovementType.OUT,
            quantity=req["quantity"]

        )
        db.add(new_movement)
        db.flush()
     db.add(new_batch)
    
     db.commit()

     return {
                "message": "Stock available",
                "Ingredients": requirements
            }



# Completa el lote, se le da la fecha de fin y la cantidad producida despues deceunta del stock de ingredientes
@router.post("/completed/{batch_id}")
def create_batch(batch_id:int, batch:BatchesCompleted, db:Session = Depends(get_db)):
     #agrego al cantidad producida tanto en el lote como en la tabla ingredientes para actuaizar el stock
     batch_up = db.scalar(select(Batch).where(Batch.id == batch_id ))
     batch_up.produced_quantity = batch.produced_quantity
     batch_up.end_date = datetime.now(timezone.utc)
     batch_up.recipe.stock_units += batch.produced_quantity
     db.flush()

          
     db.commit()
     db.refresh(batch_up)
     return batch_up


#leer todos los lotes
@router.get("/")
def read_batch( db:Session = Depends(get_db)):
     batches = db.scalars(Select(Batch).options(joinedload(Batch.recipe))).unique().all()
     return batches 

