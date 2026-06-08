"""User document model for MongoDB.

Defines what a user record looks like in the 'users' collection.
Pydantic validates all input before it reaches the database.
"""

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    """Input model for POST /register."""
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")


class UserLogin(BaseModel):
    """Input model for POST /login."""
    username: str
    password: str


class UserInDB(BaseModel):
    """What gets stored in MongoDB — password is always hashed, never plain text."""
    username: str
    hashed_password: str


class TokenResponse(BaseModel):
    """Response returned by POST /login."""
    access_token: str
    token_type: str = "bearer"
    message: str = "Login successful. Use this token in the Authorization header."
