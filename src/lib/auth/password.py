from json import loads

from bcrypt import checkpw, gensalt, hashpw
from donttrust import DontTrust, Schema, ValidationError
from fastapi import Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from prisma import Json
from src.lib.db import db
from src.lib.session import Session


class LoginBody(BaseModel):
    email: str
    password: str


async def login_handler(
    body: LoginBody = Body(...), session: Session = Depends()
) -> JSONResponse:
    try:
        schema = DontTrust(
            email=Schema().email().required(), password=Schema().string().required()
        )
        schema.validate(body.dict())
    except ValidationError as e:
        raise HTTPException(422, e.message)

    user = await db.user.find_unique(where={"email": body.email})

    if user is None:
        raise HTTPException(400, "Invalid email or password")

    if (
        user.provider != "password"
        or user.provider is None
        or not user.provider_data["password"]  # type: ignore
    ):
        raise HTTPException(
            400,
            "You can't login using a password. Please login using \""
            + (user.provider or "email")
            + '" instead.',
        )

    if not checkpw(
        body.password.encode(), user.provider_data["password"].encode()  # type: ignore
    ):
        raise HTTPException(400, "Invalid email or password")

    profile = await db.profile.find_unique(where={"id": user.id})
    if not profile:
        profile = await db.profile.create(
            data=dict(id=user.id, name=body.email.split("@")[0])  # type: ignore
        )

    session.set("user_id", user.id)
    session.set("logged_in", True)

    return JSONResponse(
        {"user": {**loads(user.json()), "profile": loads(profile.json())}}
    )


async def register_handler(
    body: LoginBody = Body(...), session: Session = Depends()
) -> JSONResponse:
    try:
        schema = DontTrust(
            email=Schema().email().required(), password=Schema().string().required()
        )
        schema.validate(body.dict())
    except ValidationError as e:
        raise HTTPException(422, e.message)

    user = await db.user.find_unique(where={"email": body.email})

    if user:
        raise HTTPException(400, "User already registered")

    user = await db.user.create(
        data={
            "email": body.email,
            "provider": "password",
            "provider_data": Json(
                {"password": hashpw(body.password.encode(), gensalt()).decode()}
            ),
            "profile": {"create": {"name": body.email.split("@")[0]}},
        }
    )

    session.set("user_id", user.id)
    session.set("logged_in", True)

    return JSONResponse({"user": loads(user.json())})
