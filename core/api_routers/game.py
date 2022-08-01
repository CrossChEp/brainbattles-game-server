from fastapi import APIRouter
from starlette.websockets import WebSocket

from core.controllers.websocket_controllers import websocket_controller

game_router = APIRouter()


@game_router.websocket('/api/game')
async def game(token: str, game_token: str,
               websocket: WebSocket):
    await websocket_controller(token, game_token, websocket)
