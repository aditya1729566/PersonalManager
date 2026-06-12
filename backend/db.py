import os
import json
import aiosqlite
from pathlib import Path


def _db_path_from_env():
    url = os.getenv("DATABASE_URL", "sqlite:///./data/kanban.db")
    # Expect format sqlite:///./path
    if url.startswith("sqlite:///"):
        path = url.replace("sqlite:///", "")
        return str(Path(path).resolve())
    return url


async def init_db():
    path = _db_path_from_env()
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(path) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS kanbans (
                username TEXT PRIMARY KEY,
                data TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                created_at REAL NOT NULL
            )
            """
        )
        await db.commit()


async def get_kanban(username: str):
    path = _db_path_from_env()
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(path) as db:
        cur = await db.execute("SELECT data FROM kanbans WHERE username = ?", (username,))
        row = await cur.fetchone()
        if row:
            data = json.loads(row[0])
            # Migrate legacy format where columns contain 'cards' arrays
            if isinstance(data, dict) and "columns" in data and data["columns"]:
                cols = data["columns"]
                # detect legacy column format using 'cards' key
                if any("cards" in c for c in cols) and "cards" not in data:
                    cards_map = {}
                    new_cols = []
                    for col in cols:
                        card_list = col.get("cards", [])
                        ids = []
                        for idx, card in enumerate(card_list):
                            # ensure each card has an id
                            cid = card.get("id") or f"card-{len(cards_map)+1}"
                            ids.append(cid)
                            cards_map[cid] = {"id": cid, "title": card.get("title", "Untitled"), "details": card.get("details", "")}
                        new_cols.append({"id": col.get("id", f"col-{len(new_cols)+1}"), "title": col.get("title", ""), "cardIds": ids})
                    migrated = {"columns": new_cols, "cards": cards_map}
                    # save migrated board
                    await save_kanban(username, migrated)
                    return migrated
            return data
        # default board matching frontend `BoardData` shape
        default = {
            "columns": [
                {"id": "col-backlog", "title": "Backlog", "cardIds": ["card-1", "card-2"]},
                {"id": "col-discovery", "title": "Discovery", "cardIds": ["card-3"]},
                {"id": "col-progress", "title": "In Progress", "cardIds": ["card-4", "card-5"]},
                {"id": "col-review", "title": "Review", "cardIds": ["card-6"]},
                {"id": "col-done", "title": "Done", "cardIds": ["card-7", "card-8"]},
            ],
            "cards": {
                "card-1": {"id": "card-1", "title": "Align roadmap themes", "details": "Draft quarterly themes with impact statements and metrics."},
                "card-2": {"id": "card-2", "title": "Gather customer signals", "details": "Review support tags, sales notes, and churn feedback."},
                "card-3": {"id": "card-3", "title": "Prototype analytics view", "details": "Sketch initial dashboard layout and key drill-downs."},
                "card-4": {"id": "card-4", "title": "Refine status language", "details": "Standardize column labels and tone across the board."},
                "card-5": {"id": "card-5", "title": "Design card layout", "details": "Add hierarchy and spacing for scanning dense lists."},
                "card-6": {"id": "card-6", "title": "QA micro-interactions", "details": "Verify hover, focus, and loading states."},
                "card-7": {"id": "card-7", "title": "Ship marketing page", "details": "Final copy approved and asset pack delivered."},
                "card-8": {"id": "card-8", "title": "Close onboarding sprint", "details": "Document release notes and share internally."}
            }
        }
        # save default
        await save_kanban(username, default)
        return default


async def save_kanban(username: str, data: dict):
    path = _db_path_from_env()
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(path) as db:
        txt = json.dumps(data)
        await db.execute(
            "INSERT INTO kanbans(username, data) VALUES(?, ?) ON CONFLICT(username) DO UPDATE SET data=excluded.data",
            (username, txt),
        )
        await db.commit()


async def create_user(username: str, password_hash: str):
    path = _db_path_from_env()
    async with aiosqlite.connect(path) as db:
        await db.execute("INSERT INTO users(username, password_hash) VALUES(?, ?)", (username, password_hash))
        await db.commit()


async def get_user_password_hash(username: str):
    path = _db_path_from_env()
    async with aiosqlite.connect(path) as db:
        cur = await db.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = await cur.fetchone()
        return row[0] if row else None


import time


async def create_session(token: str, username: str):
    path = _db_path_from_env()
    async with aiosqlite.connect(path) as db:
        await db.execute("INSERT INTO sessions(token, username, created_at) VALUES(?, ?, ?)", (token, username, time.time()))
        await db.commit()


async def get_session_username(token: str):
    if not token:
        return None
    path = _db_path_from_env()
    async with aiosqlite.connect(path) as db:
        cur = await db.execute("SELECT username FROM sessions WHERE token = ?", (token,))
        row = await cur.fetchone()
        return row[0] if row else None


async def delete_session(token: str):
    path = _db_path_from_env()
    async with aiosqlite.connect(path) as db:
        await db.execute("DELETE FROM sessions WHERE token = ?", (token,))
        await db.commit()
