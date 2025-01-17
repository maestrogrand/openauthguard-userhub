from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.db_healthcheck import check_database_connection
from src.core.logging import logger
from src.core.version import SERVICE_VERSION
from src.users.routes import auth_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager to handle application startup and shutdown.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    logger.info(f"Starting service: {settings.service_name}")
    if not check_database_connection():
        logger.error("Failed to connect to the database. Shutting down...")
        raise SystemExit("Database connection failed.")
    yield
    logger.info(f"Shutting down service: {settings.service_name}")


app = FastAPI(
    title=settings.service_name,
    description="Service for managing individual users",
    version=SERVICE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Health check endpoint to verify service and database status.

    Returns:
        dict: A status response including database and service version information.
    """
    is_db_connected = check_database_connection()
    status = "connected" if is_db_connected else "not connected"
    logger.info(f"Health check: Database is {status}.")
    return {
        "status": "up",
        "database": status,
        "version": SERVICE_VERSION,
    }


app.include_router(auth_router)
app.include_router(user_router, prefix="/users")


if __name__ == "__main__":
    logger.info(f"Starting {settings.service_name} on port {settings.port}...")
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
