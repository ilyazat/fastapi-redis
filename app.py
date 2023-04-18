import time
import os
import random

from redis import Redis
from fastapi import FastAPI

app = FastAPI()
redis = Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=os.getenv("REDIS_PORT", 6379),
    db=os.getenv("REDIS_DB", 0),
    password=os.getenv("REDIS_PASSWORD", None),
)

CACHE_TIME_SECONDS = os.getenv("CACHE_TIME_SECONDS", 5)


@app.get("/test")
async def test():
    start = time.time()
    result = fat_func()
    end = time.time()

    return f"The loop has taken {end - start} seconds. Result: {result}"


def fat_func():
    result: bytes = redis.get("result")
    if result:
        return result.decode()

    time.sleep(3)
    result: int = random.randint(1, 500)
    print(result)
    redis.setex("result", CACHE_TIME_SECONDS, result)
    return result
