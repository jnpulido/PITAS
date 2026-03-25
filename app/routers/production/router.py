from fastapi import APIRouter
from app.routers.production.recipe import router as recipes
from app.routers.production.ingredients import router as ingredients
from app.routers.production.batches import router as batches



router = APIRouter()
router.include_router(recipes, tags=["Recetas"])
router.include_router(ingredients, tags=["Ingredientes"])
router.include_router(batches, tags=["Lotes"])
