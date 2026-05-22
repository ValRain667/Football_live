import redis.asyncio as redis
from app.config import settings

_redis = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
_redis_available = True


class _RedisWrapper:
    async def get(self, key: str):
        global _redis_available
        if not _redis_available:
            return None
        try:
            return await _redis.get(key)
        except Exception:
            _redis_available = False
            return None

    async def setex(self, key: str, seconds: int, value: str):
        global _redis_available
        if not _redis_available:
            return
        try:
            await _redis.setex(key, seconds, value)
        except Exception:
            _redis_available = False


redis_client = _RedisWrapper()
