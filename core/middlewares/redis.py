"""Module that contains all functions that creates and gets redis tables"""


import json

from core.configs.config import redis, GAME


def get_redis_game_table():
    """creates and gets redis game table

    :return: Dict
    """
    try:
        r = json.loads(redis.get(GAME))
        if not r:
            r = {}
        return r
    except TypeError:
        redis.set(GAME, json.dumps({}))
        r = json.loads(redis.get(GAME))
        return r
