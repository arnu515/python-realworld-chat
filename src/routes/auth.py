from json import loads

from fastapi import APIRouter, HTTPException, Path, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse

from src.lib.auth import password, providers, util
from src.lib.db import db
from src.lib.session import Session

router = APIRouter(prefix="/api/auth")


router.add_api_route("/login", password.login_handler, methods=["POST"])
router.add_api_route("/register", password.register_handler, methods=["POST"])


# Ported from my website's source code
# https://github.com/arnu515/arnu515/blob/master/pages/api/auth/%5Bprovider%5D.ts
@router.get("/cb")
async def auth_callback(request: Request) -> RedirectResponse:
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing code or state")

    payload = util.get_code_payload(state)
    print("payload", payload)
    if type(payload) != dict or type(payload.get("provider")) != str:
        raise HTTPException(422, "Invalid request")

    Provider = providers.get(payload["provider"])
    if Provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")

    user = await Provider.get_user(code, payload, request)

    profile = await db.profile.find_unique(where={"id": user.id})
    if not profile:
        await db.profile.create(
            data=dict(id=user.id, name=user.email.split("@")[0])  # type: ignore
        )

    session: Session = request.state.session
    session.set("user_id", user.id)
    session.set("logged_in", True)
    return RedirectResponse(url="/")


@router.get("/me")
async def get_logged_in_user(request: Request) -> JSONResponse:
    session: Session = request.state.session
    if not session.get("logged_in"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = session.get("user_id")
    if not user_id:
        session.delete("logged_in")
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = await db.user.find_unique(where={"id": user_id}, include={"profile": True})
    if not user:
        session.delete("user_id")
        session.delete("logged_in")
        raise HTTPException(status_code=401, detail="Unauthorized")

    return JSONResponse(dict(user=loads(user.json())))


@router.get("/{provider}")
async def auth_provider(req: Request, provider: str = Path(...)) -> Response:
    Provider = providers.get(provider)
    if Provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return await Provider.handler(req)
