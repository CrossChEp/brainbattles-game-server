from typing import Dict

from starlette.websockets import WebSocket, WebSocketDisconnect

from core.exceptions.exceptions import NO_SUCH_GAME_EXCEPTION
from core.middlewares.redis import get_redis_game_table
from core.models.game.game_auxiliary_methods import find_opponent_id
from core.store.db_model import UserTable


def get_game_from_redis_table(user: UserTable, game_token: str):
    games = get_redis_game_table()
    if not games[game_token]:
        raise NO_SUCH_GAME_EXCEPTION
    return games[game_token][str(user.id)]


class ConnectManager:
    __instance = None

    def __init__(self):
        self.active_connections: Dict = {}

    @staticmethod
    def get_instance():
        if ConnectManager.__instance is None:
            ConnectManager.__instance = ConnectManager()
        return ConnectManager.__instance

    async def connect(self, user: UserTable, websocket: WebSocket, game_token: str):
        await websocket.accept()
        user_game = get_game_from_redis_table(user, game_token)
        if int(user_game['opponent_id']) in self.active_connections:
            self.active_connections[int(user_game['opponent_id'])].append(websocket)
            self.active_connections[user.id] = self.active_connections[int(user_game['opponent_id'])]
            return
        self.active_connections[user.id] = [websocket]

    async def disconnect(self, user: UserTable, websocket: WebSocket):
        self.active_connections[user.id].remove(websocket)

    async def disconnect_all_users(self, game_token: str,
                                   user: UserTable):
        opponent_id = find_opponent_id(game_token, user.id)
        del self.active_connections[user.id]
        del self.active_connections[opponent_id]
        raise WebSocketDisconnect
