from sqlalchemy.orm import Session
from starlette.websockets import WebSocket

from core.middlewares.database_session import generate_session
from core.models.authorization.auth_methods import get_current_user
from core.models.game.game_methods import add_user_to_game


async def websocket_controller(token: str, game_token: str,
                               websocket: WebSocket):
    session: Session = next(generate_session())
    user = get_current_user(session, token)
    await add_user_to_game(websocket, user, game_token)
