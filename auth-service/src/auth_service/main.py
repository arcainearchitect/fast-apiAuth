"""
Main FastAPI application entry point.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.database import close_database, init_database
from .config.settings import get_app_settings, get_settings

def configure_logging()->None:
    """Configure structured logging."""
    settings=get_app_settings()

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processorsJSONRenderer()
            if settings.log_format=="json" else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level)
        ),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Standard logging configuration
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(message)s",
    )


@asynccontextmanager
async def lifespan(app:FastAPI)->AsyncGenerator[None, None]:
    """
    Application lifespan context manager.

    Handles startup and shutdown events for the FastAPI application.
    This is the modern way to handle app lifecycle events.
    :param app:
    :return:
    """
    logger=structlog.get_logger(__name__)

    # Startup
    logger.info("Starting Auth Service...")

    try:
        # Initialize database
        await init_database()
        logger.info("Database initiated successfully!")

        # Other startup tasks here
        # - Initialize Redis connection
        # - Start background tasks
        # - Warm up caches

        yield

    finally:
        # Shutdown
        logger.info("Shutting down Auth Service")

        # Clean up tasks
        await close_database()
        logger.info("Database connections closed")

        # Other cleanup tasks
        # - Close Redis connections
        # - Stop background tasks
        # - Clean up temporary files

def create_application()->FastAPI:
    """
    Create and configure FastAPI application.

    This factory pattern allows for easy testing and configuration of the
    application with different settings.

    :returns:
        FastAPI: Configured FastAPI application.
    """

    settings=get_app_settings()

    # Create FastAPI app with custom configuration
    app=FastAPI(
        title=settings.title,
        description=settings.description,
        version=settings.version,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
    )

    # Middleware
    # - Authentication middleware
    # - Rate limiting middleware
    # - Request logging middleware
    # - Error handling middleware

    # Routers
    # app.include_router(auth_router, prefix=f"{settings.api_v1_prefix}/auth")
    # app.include_router(users_router, prefix=f"{settings.api_v1_prefix}/users")
    # app.include_router(admin_router, prefix=f"{settings.api_v1_prefix}/admin")

    # Add basic health check endpoint
    @app.get("/health")
    async def health_check()->dict[str, str]:
        """Health check endpoint."""
        return {
            "status":"healthy",
            "service":"auth-service"
        }

    @app.get("/")
    async def root()->dict[str, str]:
        """Root endpoint."""
        return {
            "message":"Authentication Service API",
            "version":settings.version,
            "docs":settings.docs_url or "Documentation disabled",
        }

    return app


# Create the application instance
app=create_application()


def main()->None:
    """
    Main entry point for running the application.

    This function is called when running the application directly or
    through the console script defined in pyproject.toml.
    :return:
    """
    # Logging configuration first
    configure_logging()

    # Fetch settings
    settings=get_app_settings()

    # Run the application
    uvicorn.run(
        "auth_service.main.app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )


if __name__=="__main__":
    main()