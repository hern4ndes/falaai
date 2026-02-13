from fastapi import APIRouter

from app.api.routes import auth, health, usuarios_admin, participantes

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router)
api_router.include_router(usuarios_admin.router)
api_router.include_router(participantes.router)

