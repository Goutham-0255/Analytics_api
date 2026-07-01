from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.events.routing import router as event_router
from api.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # This fires up the engine and maps tables right before the app takes requests
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(event_router, prefix="/api/events")


@app.get("/")
def read_root():
    return "hello word"


@app.get("/items/{item_id}")
def read_items(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
