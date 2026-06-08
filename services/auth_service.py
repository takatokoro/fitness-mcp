"""Authentication service — JWT token generation and password hashing.

All auth logic lives here, never inside route handlers.
Uses:
  - passlib[bcrypt] for password hashing
  - python-jose[cryptography] for JWT token generation and verification
"""

import os
import logging
from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET", "fallback-secret-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

# Password hashing — bcrypt is the industry standard
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    The hash is what gets stored in MongoDB — never the plain password.
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if a plain password matches the stored bcrypt hash.
    Returns True if they match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(username: str) -> str:
    """
    Generate a JWT token for a logged-in user.
    Token expires after JWT_EXPIRE_HOURS (24 hours).

    The token contains:
      - sub: the username
      - exp: expiry timestamp

    The token is signed with JWT_SECRET so it cannot be faked.
    """
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    payload = {"sub": username, "exp": expire}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    logger.info("JWT token created for user: %s", username)
    return token


def decode_jwt_token(token: str) -> str:
    """
    Decode and verify a JWT token.
    Returns the username if valid.
    Raises JWTError if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise JWTError("Token missing subject.")
        return username
    except JWTError as exc:
        logger.warning("JWT decode failed: %s", exc)
        raise
