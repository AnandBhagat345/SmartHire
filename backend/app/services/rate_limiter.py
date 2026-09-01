import os
import time
import uuid

from app.redis import redis_client


class RateLimiter:

    async def is_allowed(
        self,
        key: str,
        limit: int,
        window: int
    ):

        # Disable rate limiting during tests
        if os.getenv("TESTING") == "true":
            return True, 0

        current_time = time.time()

        window_start = current_time - window

        request_id = str(uuid.uuid4())

        # Remove old requests
        await redis_client.zremrangebyscore(
            key,
            0,
            window_start
        )

        # Count requests inside current window
        request_count = await redis_client.zcard(key)

        # Check limit
        if request_count >= limit:
            return False, request_count

        # Add current request
        await redis_client.zadd(
            key,
            {
                request_id: current_time
            }
        )

        # Set expiry
        await redis_client.expire(
            key,
            window
        )

        return True, request_count + 1