import redis
import json
import logging
from functools import wraps
from datetime import timedelta

logger = logging.getLogger(__name__)

# Redis client initialization
redis_client = None

def init_redis(app):
    """Initialize Redis client"""
    global redis_client
    try:
        redis_client = redis.Redis(
            host=app.config.get('REDIS_HOST', 'localhost'),
            port=app.config.get('REDIS_PORT', 6379),
            db=app.config.get('REDIS_DB', 0),
            decode_responses=True
        )
        # Test connection
        redis_client.ping()
        logger.info("Redis connection established successfully")
        return redis_client
    except Exception as e:
        logger.warning(f"Redis connection failed: {str(e)}. Continuing without caching.")
        redis_client = None
        return None

def cache_key_generator(*args, **kwargs):
    """Generate cache key from function arguments"""
    key_parts = []
    for arg in args:
        if hasattr(arg, '__name__'):  # Skip function objects
            continue
        key_parts.append(str(arg))
    for k, v in kwargs.items():
        key_parts.append(f"{k}:{v}")
    return ":".join(key_parts)

def cache_with_expiry(expiry_seconds=300, key_prefix="quiz_app"):
    """
    Decorator for caching function results with expiry
    Default expiry: 5 minutes (300 seconds)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not redis_client:
                # If Redis is not available, execute function normally
                return f(*args, **kwargs)
            
            try:
                # Generate cache key
                cache_key = f"{key_prefix}:{f.__name__}:{cache_key_generator(*args, **kwargs)}"
                
                # Try to get from cache
                cached_result = redis_client.get(cache_key)
                if cached_result:
                    logger.debug(f"Cache hit for key: {cache_key}")
                    return json.loads(cached_result)
                
                # Execute function and cache result
                result = f(*args, **kwargs)
                
                # Store in cache with expiry
                redis_client.setex(
                    cache_key, 
                    expiry_seconds, 
                    json.dumps(result, default=str)
                )
                logger.debug(f"Cached result for key: {cache_key}")
                
                return result
                
            except Exception as e:
                logger.error(f"Cache error: {str(e)}. Executing function without cache.")
                return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def invalidate_cache_pattern(pattern):
    """Invalidate all cache keys matching a pattern"""
    if not redis_client:
        return
    
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
            logger.info(f"Invalidated {len(keys)} cache keys matching pattern: {pattern}")
    except Exception as e:
        logger.error(f"Cache invalidation error: {str(e)}")

def clear_user_cache(user_id):
    """Clear all cache entries for a specific user"""
    invalidate_cache_pattern(f"quiz_app:*:user_id:{user_id}")

def clear_quiz_cache(quiz_id):
    """Clear all cache entries for a specific quiz"""
    invalidate_cache_pattern(f"quiz_app:*:quiz_id:{quiz_id}")

def clear_subject_cache(subject_id):
    """Clear all cache entries for a specific subject"""
    invalidate_cache_pattern(f"quiz_app:*:subject_id:{subject_id}")

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