#!/usr/bin/env python3
"""
Module contains the Cache class
"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Tracks numbe of calls made to a method in a Cache class
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Returns the given method after incrementing the call counter
        """

        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Tracks the call history of a method in a Cache class
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        Returns the method's output after storing its inputs &
        output
        """
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    """
    Displays the call history of a Cache class method
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    func_name = fn.__qualname__
    in_key = '{}:inputs'.format(func_name)
    out_key = '{}:outputs'.format(func_name)
    func_call_count = 0
    if redis_store.exists(func_name) != 0:
        func_call_count = int(redis_store.get(func_name))
    print('{} was called {} times:'.format(func_name, func_call_count))
    func_inputs = redis_store.lrange(in_key, 0, -1)
    func_outputs = redis_store.lrange(out_key, 0, -1)
    for func_input, func_output in zip(func_inputs, func_outputs):
        print('{}(*{}) -> {}'.format(func_name,
                                     func_input.decode('utf-x8'),
                                     func_output,))


class Cache:
    """
    Cache class
    """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
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
