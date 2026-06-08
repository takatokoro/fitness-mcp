"""MongoDB connection manager.

Uses Motor async driver for FastAPI compatibility.
Connection string loaded from .env via os.getenv().
"""

import os
import logging

logger = logging.getLogger(__name__)

MONGODB_URL = os.getenv("MONGODB_URL", "")

if not MONGODB_URL:
    logger.warning("MONGODB_URL not set — database features will not work.")
    users_collection = None
else:
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client.get_database("fitness")
        users_collection = db.get_collection("users")
        logger.info("MongoDB connection initialised.")
    except Exception as exc:
        logger.error("MongoDB connection failed: %s", exc)
        users_collection = None
