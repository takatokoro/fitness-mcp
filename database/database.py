"""MongoDB connection manager.

Provides a single shared Motor async client.
Motor is the async MongoDB driver for Python — required for FastAPI
since FastAPI runs on async (non-blocking) code.

The connection string is loaded from .env via os.getenv().
Never hardcode credentials here.
"""

import os
import logging
import motor.motor_asyncio

logger = logging.getLogger(__name__)

MONGODB_URL = os.getenv("MONGODB_URL", "")

if not MONGODB_URL:
    logger.warning("MONGODB_URL not set — database features will not work.")

# Single shared client — Motor reuses connections automatically
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL) if MONGODB_URL else None

# The 'fitness' database — collection 'users' stores registered accounts
db = client["fitness"] if client else None
users_collection = db["users"] if db else None
