import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError

from src.core.config import settings
from src.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

from src.core.dependencies import bearer_scheme

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    openapi_url="/openapi.json",
    description="Production-ready GymTracker API with clean architecture",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    contact={
        "name": "GymTracker Team",
        "email": "support@gymtracker.com",
    },
    swagger_ui_parameters={"persistAuthorization": True},
)

from src.core.dependencies import bearer_scheme


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = app._original_openapi()
    schema.setdefault("components", {})["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    app.openapi_schema = schema
    return schema


app._original_openapi = app.openapi
app.openapi = custom_openapi


# === Global Error Handlers ===

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "status_code": 422},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status_code": 500},
    )


# === CORS ===

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Routers ===

from src.routers.auth import router as auth_router
app.include_router(auth_router, prefix="/api/v1")

from src.routers.health import router as health_router
app.include_router(health_router, prefix="/api/v1/admin")

from src.routers.admin_api import admin_router
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])


# === Root ===

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
        "environment": settings.ENVIRONMENT,
    }
