import os
import redis
import json


class Cacher:
    def __init__(self):
        self.r = redis.Redis(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ["REDIS_PORT"]),
            db=0
        )
        if not self.r.ping():
            raise "Error connecting cache"

        self.json_encoder = json.JSONEncoder()

    def add_offer(self, info):
        self.r.set(info['id'], self.json_encoder.encode(info))

    def clear(self):
        self.r.flushall()
