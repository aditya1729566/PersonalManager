from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.auth import router as auth_router
from backend import db
from backend.kanban import router as kanban_router
from backend.ai_router import router as ai_router

app = FastAPI()


@app.get("/api/hello")
def hello():
    return {"message": "hello world"}


# Include auth routes
app.include_router(auth_router)
app.include_router(kanban_router)
app.include_router(ai_router)


@app.on_event("startup")
async def startup_event():
    await db.init_db()

# Serve frontend static build if present at frontend/out
try:
    app.mount("/", StaticFiles(directory="frontend/out", html=True), name="static")
except Exception:
    # If frontend/out doesn't exist during development, ignore
    pass
