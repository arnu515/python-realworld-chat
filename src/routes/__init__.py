from .auth import router as auth
from .chat import router as chat
from .settings import router as settings

routes = [auth, settings, chat]
