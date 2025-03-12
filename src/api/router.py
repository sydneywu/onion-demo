from fastapi import APIRouter

from api.endpoints import user_endpoint, comment_endpoint, auth_endpoint, ingredient_endpoint

api_router = APIRouter()

api_router.include_router(user_endpoint.router, prefix="/users", tags=["Users"])
api_router.include_router(comment_endpoint.router, prefix="/comments", tags=["Comments"])
api_router.include_router(auth_endpoint.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(ingredient_endpoint.router, prefix="/ingredients", tags=["Ingredients"])
