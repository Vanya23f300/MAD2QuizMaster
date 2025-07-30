import redis
from functools import wraps
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
redis_client = None

def init_redis(app):
    """Initialize Redis connection"""
    global redis_client
    try:
        redis_client = redis.Redis(
            host=app.config.get('REDIS_HOST', 'localhost'),
            port=app.config.get('REDIS_PORT', 6379),
            db=app.config.get('REDIS_DB', 0),
            decode_responses=True
        )
        redis_client.ping()  # Test connection
        logger.info("Redis connection established successfully")
    except redis.ConnectionError as e:
        logger.warning(f"Redis connection failed: {str(e)}. Caching will be disabled.")
        redis_client = None

def cache_with_expiry(expiry_seconds=300, key_prefix=''):
    """
    Cache decorator with expiry time
    Args:
        expiry_seconds: Time in seconds before cache expires
        key_prefix: Prefix for the cache key
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not redis_client:
                return f(*args, **kwargs)

            # Create cache key from function arguments
            cache_key = f"{key_prefix}:{f.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get cached result
            cached_result = redis_client.get(cache_key)
            if cached_result:
                logger.debug(f"Cache hit for key: {cache_key}")
                return json.loads(cached_result)
            
            # Get fresh result
            result = f(*args, **kwargs)
            
            # Cache the result
            try:
                redis_client.setex(
                    cache_key,
                    expiry_seconds,
                    json.dumps(result)
                )
                logger.debug(f"Cached result for key: {cache_key}")
            except Exception as e:
                logger.error(f"Failed to cache result: {str(e)}")
            
            return result
        return decorated_function
    return decorator

def invalidate_cache_prefix(prefix):
    """
    Invalidate all cache keys with given prefix
    """
    if not redis_client:
        return
    
    try:
        keys = redis_client.keys(f"{prefix}:*")
        if keys:
            redis_client.delete(*keys)
            logger.info(f"Invalidated {len(keys)} cache keys with prefix: {prefix}")
    except Exception as e:
        logger.error(f"Failed to invalidate cache: {str(e)}")

def clear_all_cache():
    """
    Clear all cache entries
    """
    if not redis_client:
        return
    
    try:
        redis_client.flushdb()
        logger.info("Cleared all cache entries")
    except Exception as e:
        logger.error(f"Failed to clear cache: {str(e)}")

def get_cache_stats():
    """Get Redis cache statistics"""
    if not redis_client:
        return {"status": "disconnected"}
    
    try:
        info = redis_client.info()
        return {
            "status": "connected",
            "used_memory": info.get('used_memory_human'),
            "connected_clients": info.get('connected_clients'),
            "total_commands_processed": info.get('total_commands_processed'),
            "keyspace_hits": info.get('keyspace_hits', 0),
            "keyspace_misses": info.get('keyspace_misses', 0),
            "hit_rate": round(
                info.get('keyspace_hits', 0) / max(
                    (info.get('keyspace_hits', 0) + info.get('keyspace_misses', 0)), 1
                ) * 100, 2
            )
        }
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        return {"status": "error", "error": str(e)}