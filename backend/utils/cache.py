from app.config import settings
# import redis

class Cache:
    def __init__(self):
        # self.redis = redis.Redis(...) if settings.REDIS_HOST else None
        pass

    async def get(self, key: str):
        return None

    async def set(self, key: str, value: str, expire: int = 300):
        pass

cache = Cache()
