import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.football_data import get_live_matches

live_router = APIRouter()

connected_clients = []


@live_router.websocket("/live")
async def live_ws(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            matches = await get_live_matches()
            payload = json.dumps([m.model_dump() for m in matches])
            await websocket.send_text(payload)
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
    except Exception:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
