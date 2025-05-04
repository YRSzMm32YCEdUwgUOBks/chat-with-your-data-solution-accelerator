import os
import asyncpg

_pool = None


def get_postgres_pool():
    global _pool
    if not _pool:
        _pool = asyncpg.create_pool(dsn=os.getenv("POSTGRES_CONNECTION_STRING"))
    return _pool
