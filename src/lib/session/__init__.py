from os import getenv
from typing import Optional

from fastapi import Cookie, Header, Response
from nanoid import generate

from .store import SessionStore


class Session(SessionStore):
    def __init__(
        self,
        response: Response,
        session_id: Optional[str] = Cookie(None),
        x_session_id: Optional[str] = Header(None),
    ):
        sid = session_id or x_session_id or generate("1234567890abcdefwxyz", 21)
        self.session_id = sid
        super().__init__(sid)
        response.set_cookie(
            "session_id",
            sid,
            max_age=int(getenv("SESSION_EXPIRY", str(86400 * 7))),
            httponly=True,
        )

    def reset_session(self, response: Response) -> None:
        session_id = generate("1234567890abcdefwxyz", 21)
        self.session_id = session_id
        self.reset(session_id)
        response.set_cookie(
            "session_id",
            session_id,
            max_age=int(getenv("SESSION_EXPIRY", str(86400 * 7))),
            httponly=True,
        )
