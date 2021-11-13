from .app import app  # noqa: F401
from .routes import routes

for router in routes:
    app.include_router(router)
