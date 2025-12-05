import hashlib, pickle, time
import redis
from app.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=False)

def _key(query: str, intent: str):
    h = hashlib.sha256(query.encode()).hexdigest()[:16]
    return f"helpdesk:cache:{intent}:{h}"

def get_cached(query: str, intent: str):
    val = redis_client.get(_key(query, intent))
    if not val:
        return None
    try:
        return pickle.loads(val)
    except Exception:
        return None

def set_cached(query: str, intent: str, value, ttl: int = 3600):
    try:
        redis_client.set(_key(query, intent), pickle.dumps(value), ex=ttl)
    except Exception as e:
        # best-effort caching; don't raise to avoid breaking pipeline
        print('Cache set failed', e)
