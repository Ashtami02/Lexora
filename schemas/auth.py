from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str      # user or lawyer
    country: str
    language: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(request: SignupRequest):

    # Later we'll store in PostgreSQL

    return {
        "message": "Account created successfully",
        "user": request
    }


@router.post("/login")
def login(request: LoginRequest):

    # Later we'll verify password & return JWT

    return {
        "message": "Login successful",
        "token": "jwt_token_here"
    }