from os import getenv
from urllib.parse import urlencode

import requests
from fastapi import HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from prisma.models import User

from prisma import Json
from src.lib.db import db

from .util import AuthProvider, generate_code


class Provider(AuthProvider):
    @staticmethod
    async def handler(request: Request) -> Response:
        code = generate_code({"provider": "github"})
        return RedirectResponse(
            "https://github.com/login/oauth/authorize?"
            + urlencode(
                {
                    "client_id": getenv("GITHUB_CLIENT_ID"),
                    "scope": "user:email",
                    "state": code,
                }
            )
        )

    @staticmethod
    async def get_user(  # noqa: C901
        code: str, metadata: dict, request: Request
    ) -> User:
        if metadata.get("provider") != "github":
            raise HTTPException(status_code=422, detail="Invalid request")

        # Get the oauth access token from github using the code above
        res = requests.post(
            "https://github.com/login/oauth/access_token",
            json={
                "client_id": getenv("GITHUB_CLIENT_ID"),
                "client_secret": getenv("GITHUB_CLIENT_SECRET"),
                "code": code,
                "redirect_uri": request.url_for("auth_callback"),
                "grant_type": "authorization_code",
            },
            headers={"Accept": "application/json"},
        )
        data = res.json()

        if data.get("error"):
            raise HTTPException(
                status_code=res.status_code,
                detail=data.get("error_description", data.get("error")),
            )

        if data.get("scope") != "user:email":
            raise HTTPException(status_code=422, detail="Invalid request")

        user_res = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": "token " + data.get("access_token"),
                "Accept": "application/json",
            },
        )
        user_data = user_res.json()
        if user_data.get("error"):
            raise HTTPException(
                status_code=res.status_code,
                detail=user_data.get("error_description", user_data.get("error")),
            )

        email_res = requests.get(
            "https://api.github.com/user/emails",
            headers={
                "Authorization": "token " + data.get("access_token"),
                "Accept": "application/json",
            },
        )
        email_data = email_res.json()
        if type(email_data) == dict and email_data.get("error"):
            raise HTTPException(
                status_code=email_res.status_code,
                detail=email_data.get("error_description", email_data.get("error")),
            )
        primary_email = None
        for email in email_data:
            if email.get("primary") and email.get("verified"):
                primary_email = email
        if not primary_email:
            raise HTTPException(
                status_code=400,
                detail="You need to verify and set a primary "
                "email on your Github account",
            )

        user = await db.user.find_unique(
            where={"provider_id": str(user_data.get("id"))}
        )
        if not user:
            user = await db.user.create(
                data=dict(
                    email=primary_email.get("email"),
                    provider="github",
                    provider_id=str(user_data.get("id")),
                    provider_data=Json(user_data),
                )
            )
        if user.provider != "github":
            raise HTTPException(
                status_code=400,
                detail='You can\'t login with "github". Please use "'
                + (user.provider or "email")
                + '" instead.',
            )
        if user.email != primary_email.get("email"):
            await db.user.update(
                data=dict(email=primary_email.get("email")),
                where={"id": user.id},
            )

        return user
