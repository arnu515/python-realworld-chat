from json import loads
from typing import Optional
from urllib.parse import urlparse

import requests
from fastapi import APIRouter, Body, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.lib.db import db
from src.lib.session import Session

router = APIRouter(prefix="/api/settings")


class SettingsProfileBody(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None


@router.patch("/profile")
async def settings_profile(  # noqa: C901
    request: Request, body: SettingsProfileBody = Body(...)
) -> JSONResponse:
    session: Session = request.state.session
    if not session.get("logged_in") or not session.get("user_id"):
        raise HTTPException(401, "Unauthorized")

    profile = await db.profile.find_unique(where={"id": session.get("user_id")})
    if profile is None:
        return

    if body.name:
        profile.name = body.name
    if body.avatar:
        # Check if avatar_url is from imgur or gravatar
        avatar_url = urlparse(body.avatar)
        if avatar_url.scheme != "https":
            raise HTTPException(400, "Avatar URL must be HTTPS!")
        if avatar_url.netloc not in ["i.imgur.com", "gravatar.com"]:
            raise HTTPException(400, "Avatar URL can only be from imgur or gravatar")
        # Check if avatar_url outputs an image
        res = requests.get(avatar_url.geturl())
        if not res.headers.get("content-type").startswith("image"):
            raise HTTPException(400, "The provided Avatar URL does not return an image")
        profile.avatar = body.avatar
    if body.bio:
        profile.bio = body.bio
    if body.website:
        # Check if the website is a valid url
        if not urlparse(body.website).scheme:
            raise HTTPException(400, "The provided website is not a valid URL")
        profile.website = body.website

    profile = await db.profile.update(
        data={
            "name": profile.name,
            "avatar": profile.avatar,
            "website": profile.website,
            "bio": profile.bio,
        },
        where={"id": profile.id},
    )
    return JSONResponse({"profile": loads(profile.json())})
