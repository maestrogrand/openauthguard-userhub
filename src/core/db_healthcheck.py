from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from src.core.database import engine
from src.core.logging import logger
from src.core.config import settings


def check_database_connection() -> bool:
    """
    Checks the database connection by attempting to connect to the database.
    Returns True if the connection is successful, otherwise False.
    """
    logger.info("Performing database health check...")
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Database connection successful.")
        return True
    except OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        logger.debug(f"Connection string used: {settings.get_encoded_database_url()}")
        return False
