from src.lib.db import db

from .app import app  # noqa: F401
from .routes import routes

for router in routes:
    app.include_router(router)


@app.on_event("startup")
async def connect_to_db():
    await db.connect()


@app.on_event("shutdown")
async def disconnect_from_db():
    if db.is_connected():
        await db.disconnect()
