from datetime import datetime

from pydantic import BaseModel


class BatchesBase(BaseModel):
    id:int
    start_date:datetime
    produced_quantity:int
    planned_quantity:int



class Ingredient(BaseModel):
    id: int
    name:str



class Recipe(BaseModel):
    id: Ingredient
    name:str
    stock_units:int

# class BatchesCreate(BaseModel):
#     planned_quantity:int
#     produced_quantity:int
#     end_date:datetime
#     recipe:Recipe

class BatchesCompleted(BaseModel):
      produced_quantity:int