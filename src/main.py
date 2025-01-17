from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.logging import logger
from src.core.config import settings
from src.users.routes import user_router, auth_router
from src.core.db_healthcheck import check_database_connection
from src.core.version import SERVICE_VERSION
import uvicorn

app = FastAPI(
    title=settings.service_name,
    description="Service for managing individual users",
    version=SERVICE_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify service and database status.
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


@app.on_event("startup")
async def startup_event():
    """
    Event triggered on application startup.
    Logs the service startup and performs a database health check.
    """
    logger.info(f"Starting service: {settings.service_name}")
    if not check_database_connection():
        logger.error("Failed to connect to the database. Shutting down...")
        raise SystemExit("Database connection failed.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Event triggered on application shutdown.
    Logs the service shutdown.
    """
    logger.info(f"Shutting down service: {settings.service_name}")


if __name__ == "__main__":
    logger.info(f"Starting {settings.service_name} on port {settings.port}...")
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
