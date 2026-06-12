import os
import asyncio
from backend import db


def test_init_db(tmp_path, monkeypatch):
    p = tmp_path / "data" / "kanban.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{p}")

    # run init_db
    asyncio.run(db.init_db())
    assert p.exists()


def test_get_default_kanban(tmp_path, monkeypatch):
    p = tmp_path / "data" / "kanban.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{p}")

    # ensure tables are created first
    asyncio.run(db.init_db())
    board = asyncio.run(db.get_kanban("user"))
    assert "columns" in board
    assert isinstance(board["columns"], list)