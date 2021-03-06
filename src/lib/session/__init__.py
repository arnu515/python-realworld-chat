from fastapi import Response
from nanoid import generate

from .store import SessionStore


class Session(SessionStore):
    @staticmethod
    def generate_sid():
        return generate("qwertyuiopasdfghjklzxcvbnm1234567890", 32)

    @staticmethod
    def set_session_cookie(sid: str, response: Response) -> Response:
        response.set_cookie("sid", sid, max_age=7 * 86400, httponly=True)
        return response

    def refresh_session(self, response: Response) -> Response:
        """
        Resets the session entirely by generating a new SID.
        It is your duty to return the response returned by this method
        """
        self.reset(self.generate_sid())
        return self.set_session_cookie(self.session_id, response)
