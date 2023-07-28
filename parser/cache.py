import os

import redis


class Cacher:
    def __init__(self):
        self.r = redis.Redis(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ["REDIS_PORT"])
        )
        if not self.r.ping():
            print("Error connecting cache")
        else:
            print("Connected to cache successfully")
