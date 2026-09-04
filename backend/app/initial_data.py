"""Initialize application database data such as the owner account and predefined genres."""
import logging
from sqlmodel import Session
from app.core.db import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    """Open a database session and run the initial data setup."""
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    """Run database initialization with logging."""
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()