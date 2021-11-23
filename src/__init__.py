import os
from typing import Callable

from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware

from src.lib.db import db
from src.lib.session import Session

from .app import app  # noqa: F401
from .routes import routes

if bool(os.getenv("ENABLE_CORS")) or bool(os.getenv("DEBUG")):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

for router in routes:
    app.include_router(router)


@app.middleware("http")
async def session_middleware(request: Request, call_next: Callable) -> Response:
    sid = (
        request.cookies.get("sid")
        or request.headers.get("x-sid")
        or Session.generate_sid()
    )
    request.state.session = Session(sid)
    response: Response = await call_next(request)
    response = Session.set_session_cookie(sid, response)
    return response


@app.on_event("startup")
async def connect_to_db():
    await db.connect()


@app.on_event("shutdown")
async def disconnect_from_db():
    if db.is_connected():
        await db.disconnect()
