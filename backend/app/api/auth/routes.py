"""
Authentication Routes
=====================
JWT-based user authentication.
"""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import jwt
import hashlib

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer()

USERS_FILE = Path("backend/app/data/users.json")
USERS_FILE.parent.mkdir(parents=True, exist_ok=True)

SECRET_KEY = "agriScan-secret-key-2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    token: str
    user: dict


def load_users() -> dict:
    if not USERS_FILE.exists():
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/register", response_model=TokenResponse)
async def register(user: UserRegister):
    users = load_users()
    
    if any(u["email"] == user.email for u in users.values()):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = str(uuid.uuid4())
    users[user_id] = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
        "created_at": datetime.utcnow().isoformat(),
        "history": []
    }
    
    save_users(users)
    token = create_token(user_id)
    
    return {
        "token": token,
        "user": {
            "id": user_id,
            "name": user.name,
            "email": user.email
        }
    }


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin):
    users = load_users()
    
    user_record = None
    for u in users.values():
        if u["email"] == user.email and u["password"] == hash_password(user.password):
            user_record = u
            break
    
    if not user_record:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user_record["id"])
    
    return {
        "token": token,
        "user": {
            "id": user_record["id"],
            "name": user_record["name"],
            "email": user_record["email"]
        }
    }


@router.get("/me")
async def get_me(user_id: str = Depends(get_current_user)):
    users = load_users()
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users[user_id]
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"]
    }
