import os
import pytest
import httpx

from backend.ai import call_openrouter


@pytest.mark.asyncio
async def test_call_openrouter_mock(monkeypatch):
    # Ensure no API key -> mock path
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    res = await call_openrouter("2+2")
    assert res["mock"] is True
    assert "4" in res["output"]


@pytest.mark.asyncio
async def test_call_openrouter_http(monkeypatch):
    # Provide dummy API key and monkeypatch httpx AsyncClient.post
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")

    class DummyResp:
        def __init__(self, data):
            self._data = data

        def json(self):
            return self._data

        def raise_for_status(self):
            return None

    async def fake_post(self, url, json=None, headers=None):
        return DummyResp({"choices": [{"message": {"content": "4"}}]})

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    res = await call_openrouter("2+2")
    assert res["mock"] is False
    assert res["output"] == "4"
