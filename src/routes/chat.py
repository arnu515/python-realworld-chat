from json import loads

from fastapi import APIRouter, Depends, HTTPException, Request, WebSocketDisconnect
from fastapi.responses import JSONResponse
from prisma.models import ChatRequest, User
from pydantic import BaseModel

from src.lib.db import db
from src.lib.ws import WebSocket

router = APIRouter()


@router.websocket("/ws/main")
async def websocket_endpoint(socket: WebSocket = Depends(WebSocket.connect)):
    try:
        while True:
            data = await socket.ws.receive_json()
            print(data)
    except WebSocketDisconnect:
        if WebSocket.connections().get(socket.id):
            WebSocket.connections().pop(socket.id)
        print("WebSocket disconnected")


class ChatRequestBody(BaseModel):
    identifier: str


@router.get("/api/chat/requests")
async def get_chat_requests(request: Request):
    def clean_user(user: User):
        return {"id": user.id, "email": user.email, "profile": user.profile}

    def map_requests(req: ChatRequest):
        req.from_user = clean_user(req.from_user)  # type: ignore
        req.to_user = clean_user(req.to_user)  # type: ignore
        return loads(req.json())

    session = request.state.session
    if not session.get("logged_in") or not session.get("user_id"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    sent_chat_requests = await db.chatrequest.find_many(
        where={"from_user_id": session.get("user_id"), "accepted": False},
        include={
            "from_user": {"include": {"profile": True}},
            "to_user": {"include": {"profile": True}},
        },
    )
    recv_chat_requests = await db.chatrequest.find_many(
        where={"to_user_id": session.get("user_id"), "accepted": False},
        include={
            "from_user": {"include": {"profile": True}},
            "to_user": {"include": {"profile": True}},
        },
    )
    return JSONResponse(
        {
            "sent": list(map(map_requests, sent_chat_requests)),
            "received": list(map(map_requests, recv_chat_requests)),
        }
    )


@router.post("/api/chat/requests")
async def create_chat_request(body: ChatRequestBody, request: Request) -> JSONResponse:
    session = request.state.session
    if not session.get("logged_in") or not session.get("user_id"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = await db.user.find_unique(where={"id": body.identifier.strip()})
    if not user:
        user = await db.user.find_unique(where={"email": body.identifier.strip()})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    req = await db.chatrequest.find_first(
        where={"from_user_id": session.get("user_id"), "to_user_id": user.id}
    )
    if req:
        raise HTTPException(status_code=400, detail="You've already sent a request")

    req = await db.chatrequest.create(
        data={  # type: ignore
            "from_user_id": session.get("user_id"),
            "to_user_id": user.id,
        }
    )

    # check if the opposite user is connected in the websocket
    # if so, send them a message
    opp_ws = WebSocket.connections().get(user.id)
    if opp_ws:
        await opp_ws.ws.send_json({"type": "chat_request", "req": req.json()})

    return JSONResponse(status_code=201, content={"req": req.dict()})


class AcceptOrDeclineChatRequestBody(BaseModel):
    id: str
    action: str


@router.patch("/api/chat/requests")
async def accept_or_decline_chat_request(
    body: AcceptOrDeclineChatRequestBody, request: Request
) -> JSONResponse:
    session = request.state.session
    if not session.get("logged_in") or not session.get("user_id"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    req = await db.chatrequest.find_unique(where={"id": body.id})
    if not req or req.accepted:
        raise HTTPException(status_code=404, detail="Chat Request not found")

    if body.action not in ["accept", "decline"]:
        raise HTTPException(status_code=400, detail="Invalid action")

    if body.action == "accept":
        req = await db.chatrequest.update(
            data={"accepted": True}, where={"id": body.id}
        )
        # if user is connected in websocket, send message
        if WebSocket.connections().get(req.from_user_id):  # type: ignore
            WebSocket.connections().get(req.from_user_id).ws.send_json(  # type: ignore
                {"type": "chat_request_accepted", "req": req.json()}  # type: ignore
            )
    elif body.action == "decline":
        req = await db.chatrequest.delete(where={"id": body.id})
        # if user is connected in websocket, send message
        if WebSocket.connections().get(req.from_user_id):  # type: ignore
            WebSocket.connections().get(req.from_user_id).ws.send_json(  # type: ignore
                {"type": "chat_request_declined", "req": req.json()}  # type: ignore
            )

    return JSONResponse(status_code=200, content={"req": req.dict()})  # type: ignore
