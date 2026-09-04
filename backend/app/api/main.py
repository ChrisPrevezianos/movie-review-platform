"""API router configuration for all application endpoints."""
from fastapi import APIRouter
from app.api.routes import login, users, genres, actors, directors, reviews, movies

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(genres.router)
api_router.include_router(actors.router)
api_router.include_router(directors.router)
api_router.include_router(reviews.router)
api_router.include_router(movies.router)