import redis
import json
import logging
from typing import Optional, Any
from datetime import timedelta
import os

logger = logging.getLogger(__name__)

class CacheService:
    """
    Redis cache with in-memory fallback for premium streaming performance.
    """
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.memory_cache: dict = {}  # Fallback in-memory cache
        self.use_redis = False
        
        # Try to connect to Redis
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            try:
                self.redis_client = redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2
                )
                # Test connection
                self.redis_client.ping()
                self.use_redis = True
                logger.info("✅ Redis connected successfully")
            except Exception as e:
                logger.warning(f"⚠️ Redis unavailable, using in-memory cache: {e}")
                self.redis_client = None
        else:
            logger.info("ℹ️ REDIS_URL not set, using in-memory cache")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache (Redis or memory)."""
        try:
            if self.use_redis and self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            else:
                # In-memory fallback
                return self.memory_cache.get(key)
        except Exception as e:
            logger.error(f"Cache GET error for {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 600):
        """
        Set value in cache with TTL (default 10 minutes).
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time to live in seconds (default 600 = 10 minutes)
        """
        try:
            serialized = json.dumps(value)
            
            if self.use_redis and self.redis_client:
                self.redis_client.setex(key, ttl, serialized)
            else:
                # In-memory fallback (no TTL enforcement for simplicity)
                self.memory_cache[key] = value
                
                # Simple memory cleanup: keep only last 1000 items
                if len(self.memory_cache) > 1000:
                    # Remove oldest 200 items
                    keys_to_remove = list(self.memory_cache.keys())[:200]
                    for k in keys_to_remove:
                        del self.memory_cache[k]
        except Exception as e:
            logger.error(f"Cache SET error for {key}: {e}")
    
    async def delete(self, key: str):
        """Delete key from cache."""
        try:
            if self.use_redis and self.redis_client:
                self.redis_client.delete(key)
            else:
                self.memory_cache.pop(key, None)
        except Exception as e:
            logger.error(f"Cache DELETE error for {key}: {e}")
    
    async def clear(self):
        """Clear all cache."""
        try:
            if self.use_redis and self.redis_client:
                self.redis_client.flushdb()
            else:
                self.memory_cache.clear()
        except Exception as e:
            logger.error(f"Cache CLEAR error: {e}")

# Global cache instance
cache = CacheService()
