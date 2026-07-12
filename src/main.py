import os
import re
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from src.core.config import settings
from src.core.logging import setup_logging
from src.core.errors import error_response, ErrorCode

setup_logging()
logger = logging.getLogger(__name__)

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


# === Global Error Handlers ===

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        content = exc.detail
    else:
        content = error_response(exc.status_code, str(exc.detail))
    return JSONResponse(status_code=exc.status_code, content=content)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    messages = []
    for e in exc.errors():
        loc = " -> ".join(str(x) for x in e.get("loc", []))
        msg = e.get("msg", "")
        messages.append(f"{loc}: {msg}" if loc else msg)
    content = error_response(422, "; ".join(messages), ErrorCode.VALIDATION_ERROR)
    return JSONResponse(status_code=422, content=content)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    msg = str(exc.orig)
    match = re.search(r"UNIQUE constraint failed:\s+(\S+)", msg)
    if match:
        column = match.group(1).split(".")[-1].replace("_", " ").title()
        friendly = f"A record with this {column} already exists"
    elif re.search(r"duplicate key", msg, re.IGNORECASE):
        friendly = "A record with this value already exists"
    else:
        friendly = "Database integrity error"
    content = error_response(409, friendly, ErrorCode.CONFLICT)
    return JSONResponse(status_code=409, content=content)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    content = error_response(500, "Internal server error", ErrorCode.INTERNAL_ERROR)
    return JSONResponse(status_code=500, content=content)


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

from src.routers.admin_users import router as admin_users_router
app.include_router(admin_users_router, prefix="/api/v1/admin", tags=["Admin - Users"])

from src.routers.public_api import router as public_router
app.include_router(public_router, prefix="/api/v1", tags=["Public Catalog"])

from src.routers.media import router as media_router
app.include_router(media_router, prefix="/api/v1/admin", tags=["Admin - Media"])

from src.routers.users import router as users_router
app.include_router(users_router, prefix="/api/v1", tags=["Users"])

from src.routers.workouts import router as workouts_router
app.include_router(workouts_router, prefix="/api/v1", tags=["Workouts"])


# === Static Files (local dev) ===

if settings.STORAGE_BACKEND == "local":
    os.makedirs(settings.MEDIA_DIR, exist_ok=True)
    app.mount("/media", StaticFiles(directory=settings.MEDIA_DIR), name="media")


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
