from fastapi import APIRouter, HTTPException, Response, Request
from pydantic import BaseModel
from . import db
import hashlib
import os
import uuid

router = APIRouter()


class LoginData(BaseModel):
    username: str
    password: str


def _hash_password(username: str, password: str) -> str:
    # simple salted hash for MVP
    salt = os.getenv("PASSWORD_SALT", "pm_salt")
    s = f"{username}:{password}:{salt}"
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


@router.post("/api/register")
async def register(data: LoginData):
    existing = await db.get_user_password_hash(data.username)
    if existing:
        raise HTTPException(status_code=400, detail="User exists")
    ph = _hash_password(data.username, data.password)
    await db.create_user(data.username, ph)
    return {"success": True}


@router.post("/api/login")
async def login(data: LoginData, response: Response):
    ph = await db.get_user_password_hash(data.username)
    if not ph:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if ph != _hash_password(data.username, data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = uuid.uuid4().hex
    await db.create_session(token, data.username)
    response.set_cookie(key="session", value=token, httponly=True, path="/", samesite="lax")
    return {"success": True}


@router.post("/api/logout")
async def logout(request: Request, response: Response):
    token = request.cookies.get("session")
    if token:
        await db.delete_session(token)
    response.delete_cookie("session", path="/")
    return {"success": True}


@router.get("/api/session")
async def session(request: Request):
    token = request.cookies.get("session")
    username = await db.get_session_username(token)
    if username:
        return {"user": username}
    raise HTTPException(status_code=401, detail="Not authenticated")
