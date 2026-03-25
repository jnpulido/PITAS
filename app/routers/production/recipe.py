from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from websockets import route

from app.db import get_db
from app.models import Recipe, RecipeIngredient  
from app.schemes.recipe import RecipeCreate, RecipeResponse


router = APIRouter(
    prefix="/recipes",
    tags=["Recetas"],
)

#para crear recetas
@router.post(
    "/create",
    description="Crea una receta",
    response_model=RecipeResponse,
    status_code=201,
)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = Recipe(
        name=recipe.name,
        quantity_base=recipe.quantity_base,
        stock_units = recipe.stock_units,
    ) 
    db.add(new_recipe)
    db.flush()
  
    for item in recipe.recipe_ingredients:
      
        recipe_ingredients = RecipeIngredient(
            recipe_id = new_recipe.id,
            ingredient_id=item.ingredient_id,
            quantity=item.quantity,
            
        )
       
        db.add(recipe_ingredients)
   
    db.commit()
    db.refresh(new_recipe)

    recipe = db.scalar(
    select(Recipe)
    .where(Recipe.id == new_recipe.id)
    .options(
        joinedload(Recipe.recipe_ingredients).joinedload(RecipeIngredient.ingredient)
    )
)
    return recipe

# para mostar todas las recetas
@router.get("/",description="muestra todas las recetas creadas",response_model=list[RecipeResponse], status_code=201)
async def rad_recipe(db: Session = Depends(get_db)):
    
    recipes = db.scalars(
        select(Recipe).options(
            joinedload(Recipe.recipe_ingredients).joinedload(RecipeIngredient.ingredient)
        )
    ).unique().all()

    return recipes



# calculador de ingredientes
# @router.get()
