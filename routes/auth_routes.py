"""Authentication routes — /register and /login.

These two routes are public (no JWT token required).
All other fitness routes require a valid JWT token in V2.

POST /register — create a new user account
POST /login    — return a JWT token
"""

import logging

from fastapi import APIRouter, HTTPException

from database.database import users_collection
from database.user_document import UserRegister, UserLogin, TokenResponse
from services.auth_service import hash_password, verify_password, create_jwt_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["auth"])


@router.post("/register", operation_id="register_user")
async def register(user: UserRegister):
    """
    Create a new user account.

    - Checks if username already exists in MongoDB
    - Hashes the password with bcrypt before saving
    - Stores {username, hashed_password} in the 'users' collection
    - Never stores the plain text password

    Args:
        user: UserRegister model with username and password.

    Returns:
        Success message on registration.
        403 if username already taken.
        503 if database is unavailable.
    """
    if users_collection is None:
        raise HTTPException(status_code=503, detail="Database not configured.")

    # Check if username already exists
    existing = await users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=403, detail=f"Username '{user.username}' already taken.")

    # Hash password and save to MongoDB
    hashed = hash_password(user.password)
    await users_collection.insert_one({
        "username": user.username,
        "hashed_password": hashed,
    })

    logger.info("New user registered: %s", user.username)
    return {"message": f"User '{user.username}' registered successfully."}


@router.post("/login", response_model=TokenResponse, operation_id="login_user")
async def login(user: UserLogin):
    """
    Login and receive a JWT token.

    - Looks up username in MongoDB
    - Verifies password against stored bcrypt hash
    - Returns a JWT token valid for 24 hours

    The token must be sent in subsequent requests as:
        Authorization: Bearer <token>

    Args:
        user: UserLogin model with username and password.

    Returns:
        TokenResponse with access_token and token_type.
        401 if credentials are invalid.
        503 if database is unavailable.
    """
    if users_collection is None:
        raise HTTPException(status_code=503, detail="Database not configured.")

    # Look up user
    db_user = await users_collection.find_one({"username": user.username})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    # Verify password
    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    # Generate JWT token
    token = create_jwt_token(user.username)
    logger.info("User logged in: %s", user.username)

    return TokenResponse(access_token=token)
