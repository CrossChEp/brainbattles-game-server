from core.middlewares.redis import get_redis_game_table


def find_opponent_id(game_token: str, user_id: int) -> int:
    games = get_redis_game_table()
    opponent_id = games[game_token][str(user_id)]['opponent_id']
    return int(opponent_id)
