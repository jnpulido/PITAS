
from decimal import Decimal
from typing import List
from pydantic import BaseModel, Field, ConfigDict




class IngredientPriceBase(BaseModel):
    price:Decimal

class IngredientsBase(BaseModel): 
    name:str
    unit:str
    stock:int


class IngredientPriceResponse(BaseModel):
    price:Decimal
    model_config = ConfigDict(from_attributes=True)

# ✅   
#crear ingrediente coon su primer precio
class IngredientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    unit:str 
    stock:int
    ingredients_price:IngredientPriceBase
   

# ✅
class IngredientResponse(BaseModel):
    id: int
    name: str
    unit:str
    stock:int
    ingredients_price:list[IngredientPriceResponse]
    model_config = ConfigDict(from_attributes=True)


# ✅
class NewPriceCreate(IngredientPriceBase):
    stock:int
    price: Decimal



# class IngredientResponseComplete(IngredientResponse):
#     price:Decimal
#     quantity:float

# class IngredientStockCreate(BaseModel):
#     quantity:int
#     ingredient_id: int

# class IngredientStockResponse(BaseModel):
#     quantity:float

# class IngredientAllResponse(IngredientResponse):
#     price_ingredients:List[PriceIngredientResponse]
#     ingredient_stock: IngredientStockResponse