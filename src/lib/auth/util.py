import os
from json import JSONDecodeError, dumps, loads
from typing import Optional

from fastapi import Request, Response
from nanoid import generate
from prisma.models import User

from src.lib.rd import rd


class AuthProvider:
    @staticmethod
    async def handler(request: Request) -> Response:
        """
        Called when the user visits /api/auth/provider
        """
        pass

    @staticmethod
    async def get_user(code: str, metadata: dict, request: Request) -> User:
        """
        Second part of the flow.
        :return: User's ID and if it should redirect
        """
        pass


def generate_code(payload: dict, length: int = 21) -> str:
    code = generate("abcdefghjklmnopqrstuvwxyz", length)
    rd.hset("auth-codes", code, dumps(payload))
    rd.expire("auth-codes", int(os.getenv("SESSION_EXPIRY", str(86400 * 7))))
    return code


def get_code_payload(code: str) -> Optional[dict]:
    try:
        from_rd = rd.hget("auth-codes", code)
        if not from_rd:
            return None
        data = loads(from_rd)
        rd.hdel("auth-codes", code)
        rd.expire("auth-codes", int(os.getenv("SESSION_EXPIRY", str(86400 * 7))))
        return data
    except JSONDecodeError:
        rd.hdel("auth-codes", code)
        rd.expire("auth-codes", int(os.getenv("SESSION_EXPIRY", str(86400 * 7))))
        return None
