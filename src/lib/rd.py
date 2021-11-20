from os import getenv

import redis

rd = redis.StrictRedis(
    host=getenv("RD_HOST", "localhost"),
    port=int(getenv("RD_PORT", "6379")),
    db=int(getenv("RD_DB", "0")),
    password=getenv("RD_PW") or None,
)
