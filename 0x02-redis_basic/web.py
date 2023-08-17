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


def cache(method: Callable) -> Callable:
    """
    Caches the fetched data
    """
    @wraps(method)
    def invoker(url) -> str:
        """
        Wrapper function for caching the output
        """
        redis_db.incr("count:{}".format(url))
        result = redis_db.get("result:{}".format(url))
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_db.set("count:{}".format(url), 0)
        redis_db.setex("result:{}".format(url), 10, result)
        return result
    return invoker


@cache
def get_page(url: str) -> str:
    """
    """
    return requests.get(url).text
