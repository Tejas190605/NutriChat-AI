import redis
import structlog

from src.config.settings import settings

logger = structlog.get_logger()

# Shared connection pool setup
pool = redis.ConnectionPool.from_url(
    settings.REDIS_URL,
    max_connections=50,
    decode_responses=True,
)


def get_redis_client() -> redis.Redis:
    """Retrieves a client mapping to the Redis connection pool.

    Returns:
        A Redis client connection instance.
    """
    return redis.Redis(connection_pool=pool)


def check_redis_health() -> bool:
    """Performs a diagnostic ping request to Redis.

    Returns:
        True if the host responds successfully, False otherwise.
    """
    client = get_redis_client()
    try:
        return bool(client.ping())
    except redis.RedisError as e:
        logger.error("Redis ping diagnostic failed", error=str(e))
        return False
