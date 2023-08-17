#!/usr/bin/env python3
"""
Module contains the Cache class
"""
import redis


class Cache:
    """
    Cache class
    """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)
