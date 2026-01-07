"""
FastAPI application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.config.logging import setup_logging
from app.config.settings import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    setup_logging()
    # TODO: Initialize database connection pool
    # TODO: Initialize Redis connection
    # TODO: Load ML models if needed

    yield

    # Shutdown
    # TODO: Close database connection pool
    # TODO: Close Redis connection


app = FastAPI(
    title="MedAdReview API",
    description="Medical Advertisement Review AI Agent API",
    version="1.0.0",
    docs_url="/docs" if settings.app_debug else None,
    redoc_url="/redoc" if settings.app_debug else None,
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.app_env,
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "MedAdReview API",
        "version": "1.0.0",
        "docs": "/docs" if settings.app_debug else None,
    }


# TODO: Include API routers
# from app.api.v1.router import api_router
# app.include_router(api_router, prefix="/api/v1")
