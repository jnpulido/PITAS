from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload


from app.models import Recipe, RecipeIngredient

def ingredients_requirements(recipe_id,planned_quantity, db:Session):
    recipe = db.scalar(
        select(Recipe)
        .where(Recipe.id == recipe_id)
        .options(joinedload(Recipe.recipe_ingredients).joinedload(RecipeIngredient.ingredient)))
    prom = planned_quantity / recipe.quantity_base 
    print(prom)
    result =[]
    for recipe_item in recipe.recipe_ingredients:
        required_quantity = recipe_item.quantity * prom
        stock_available = recipe_item.ingredient.stock

        result.append({
            "id": recipe_item.ingredient.id,
            "ingredient": recipe_item.ingredient.name,
            "quantity": required_quantity,
            "unit": recipe_item.ingredient.unit,
            "stock_available":  stock_available 
        })

    return result


def validate_ingredient_stock(result: list[dict]) -> None:
    insufficient_stock = []

    for item in result:
        if item["quantity"] > item["stock_available"]:
            insufficient_stock.append({
                "ingredient_id": item["id"],
                "ingredient_name": item["ingredient"],
                "required_quantity": item["quantity"],
                "stock_available": item["stock_available"],
                "unit": item["unit"],
            })

    if insufficient_stock:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Insufficient stock for one or more ingredients",
                "ingredients": insufficient_stock
            }
        )