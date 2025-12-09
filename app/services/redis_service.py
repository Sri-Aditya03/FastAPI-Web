import redis
from datetime import timedelta

# Connect to Redis
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

# Token expiry time (5 hours to match JWT)
TOKEN_EXPIRY = timedelta(hours=5)


def store_token(user_id: str, token: str):
    """Store token in Redis with expiry"""
    redis_client.setex(f"token:{user_id}", TOKEN_EXPIRY, token)


def get_token(user_id: str):
    """Get token from Redis"""
    return redis_client.get(f"token:{user_id}")


def delete_token(user_id: str):
    """Delete token from Redis (logout)"""
    redis_client.delete(f"token:{user_id}")


def blacklist_token(token: str, expiry_seconds: int = 18000):
    """Blacklist a token (for logout)"""
    redis_client.setex(f"blacklist:{token}", expiry_seconds, "1")


def is_token_blacklisted(token: str):
    """Check if token is blacklisted"""
    return redis_client.exists(f"blacklist:{token}") > 0
