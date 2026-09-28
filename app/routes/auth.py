from fastapi import APIRouter, HTTPException, status

from app.database import users_collection
from app.schemas.user import UserSignup, UserLogin
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/signup")
def signup(user: UserSignup):
    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "role": user.role
    }

    result = users_collection.insert_one(user_data)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
        "role": user.role
    }


@router.post("/login")
def login(user: UserLogin):
    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        existing_user["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        str(existing_user["_id"]),
        existing_user["role"]
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "role": existing_user["role"]
    }