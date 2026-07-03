#!/usr/bin/env python3
"""Initialize the database and create all tables"""

from database import init_db, engine, Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Create all database tables"""
    logger.info("Initializing database...")

    try:
        init_db()
        logger.info("✓ Database initialized successfully!")
        logger.info(f"✓ Database location: sqlite:///./loan_applications.db")
        logger.info("✓ Tables created:")
        logger.info("  - applications")
        logger.info("  - applicant_cache")
        logger.info("  - risk_assessments")
        logger.info("  - decisions")
        logger.info("  - notifications")

    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    main()
