#!/usr/bin/env python3
"""
Module contains an implementation of an expiring web cache
and tracker
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_db = redis.Redis()
"""
Redis instance
"""


def cacher(method: Callable) -> Callable:
    """
    Caches the fetched data
    """
    @wraps(method)
    def invoker(url) -> str:
        """
        Wrapper function for caching the output
        """
        redis_db.incr(f'count:{url}')
        result = redis_db.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_db.set(f'count:{url}', 0)
        redis_db.setex(f'result:{url}', 10, result)
        return result
    return invoker


@cacher
def get_page(url: str) -> str:
    """
    Get page function that uses requests to get given url
    """
    redis_db.incr(f'count:{url}')
    return requests.get(url).text
