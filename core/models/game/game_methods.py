from starlette.websockets import WebSocket

from core.exceptions.exceptions import NO_SUCH_GAME_EXCEPTION
from core.middlewares.redis import get_redis_game_table
from core.models.websockets.game import ConnectManager
from core.store.db_model import UserTable


async def add_user_to_game(websocket: WebSocket,
                           user: UserTable, game_token: str):
    connect_manager = ConnectManager.get_instance()

    await connect_manager.connect(user, websocket, game_token)
    while True:
        data = await websocket.receive_text()
        for socket in connect_manager.active_connections[user.id]:
            await socket.send_text(data)
