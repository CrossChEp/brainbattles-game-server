from sqlalchemy.orm import Session
from starlette.websockets import WebSocket

from core.configs.config import ranks
from core.middlewares.database_session import generate_session
from core.middlewares.redis import get_redis_game_table
from core.models.tasks_methods import get_task_by_id
from core.models.websockets.game import ConnectManager
from core.store.db_model import UserTable, TaskTable


async def add_user_to_game(websocket: WebSocket,
                           user: UserTable, game_token: str):
    connect_manager = ConnectManager.get_instance()

    await connect_manager.connect(user, websocket, game_token)
    while True:
        answer = await websocket.receive_text()
        if check_right_answer(answer, game_token):
            session: Session = next(generate_session())
            winning_message = f'{user.nickname} wins'
            await send_message_to_all(user, winning_message)
            task = get_game_task_by_token(game_token)
            set_winner(user, task, session)
            session.commit()
            await connect_manager.disconnect_all_users(game_token, user)


async def send_message_to_all(user: UserTable, message: str):
    socket_manager = ConnectManager.get_instance()
    for socket in socket_manager.active_connections[user.id]:
        await socket.send_text(message)


def check_right_answer(answer: str, game_token: str):
    task = get_game_task_by_token(game_token)
    if answer == task.right_answer:
        return True
    return False


def get_game_task_by_token(game_token: str):
    games = get_redis_game_table()
    game_users = list(games[game_token].keys())
    task = get_task_by_id(games[game_token][game_users[0]]['task_id'])
    return task


def set_winner(user: UserTable, task: TaskTable, session: Session):
    user = session.query(UserTable).filter_by(id=user.id).first()
    user.wins += 1
    user.scores += task.scores
    user.games += 1
    session.commit()


def improve_rank(user: UserTable):
    ranks_scores_list = list(ranks.keys())
    for score, index in ranks_scores_list:
        if user.scores < ranks_scores_list[index + 1]:
            user.rank = ranks[score]
            break
