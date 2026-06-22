from fastapi import FastAPI
from src.routers.health import router as health_router
import os
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    openapi_url="/openapi.json",
    description="Production-ready GymTracker API with clean architecture",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    contact={
        "name": "GymTracker Team",
        "email": "support@gymtracker.com"
    }
)

from src.routers.auth import router as auth_router
app.include_router(auth_router, prefix="/api/v1")

app.include_router(health_router, prefix="/api/v1/admin")

from src.routers.admin_api import admin_router
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
        "environment": settings.ENVIRONMENT
    }


from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
