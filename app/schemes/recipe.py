
from typing import Optional
from pydantic import BaseModel, ConfigDict




class RecipeBase(BaseModel):
    name:str
    quantity_base:int
    stock_units:int

class RecipeIngredientCreate(BaseModel):
    ingredient_id: int
    quantity: float
    


class RecipeCreate(BaseModel):
    name: str
    quantity_base: int
    stock_units: int
    recipe_ingredients: list[RecipeIngredientCreate]


class ingredientResponse(BaseModel):
    id:int
    name: str
    model_config= ConfigDict(from_attributes=True)


class RecipeIngredientResponse(BaseModel):
    quantity:int
    ingredient:ingredientResponse
    model_config= ConfigDict(from_attributes=True)
    


class RecipeResponse(BaseModel):
    id:int
    name: str
    quantity_base: int
    stock_units: int
    recipe_ingredients: list[RecipeIngredientResponse]
    model_config = ConfigDict(from_attributes=True)

# class RecipeUpdate(BaseModel):
#     name: Optional[str] = None
#     quantity_produced: Optional[int] = None
#     validity: Optional[bool] = None

# class RecipeRead(RecipeBase):
#     id: int 

