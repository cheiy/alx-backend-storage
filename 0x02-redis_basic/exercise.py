#!/usr/bin/env python3
"""
Module contains the Cache class
"""
import redis
import uuid
from typing import Union, Callable


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

    def get(self, key: str, fn: Callable = None) ->\
            Union[str, bytes, int, float]:
        """
        Method takes a key string argument and an optional Callable argument
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """
        Method automatically parameterizes Cache.get with the correct
        conversion function for strings - in this case decode
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Method automatically parameterizes Cache.get with the correct
        conversion function for integers
        """
        return self.get(key, lambda x: int(x))
