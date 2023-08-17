#!/usr/bin/env python3
"""
Module contains the Cache class
"""
import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class
    """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a value in Redis and returns a unique key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
