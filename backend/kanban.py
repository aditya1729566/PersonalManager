from fastapi import APIRouter, Request, HTTPException
from typing import Any
from . import db

router = APIRouter()


@router.get("/api/kanban")
async def read_kanban(request: Request) -> Any:
    token = request.cookies.get("session")
    username = await db.get_session_username(token)
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await db.get_kanban(username)


@router.put("/api/kanban")
async def write_kanban(payload: dict, request: Request) -> Any:
    token = request.cookies.get("session")
    username = await db.get_session_username(token)
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    await db.save_kanban(username, payload)
    return {"success": True}
