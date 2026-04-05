"""Корневой APIRouter: подключает маршруты v1 и служебные."""

from fastapi import APIRouter

from backend.api.routers import health
from backend.api.routers.v1 import v1_router

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(v1_router)
