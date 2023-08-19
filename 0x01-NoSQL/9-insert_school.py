#!/usr/bin/env python3
"""
Module contains a function that inserts a document
"""


def insert_school(mongo_collection, **kwargs):
    """
    Function inserts a document
    """
    post = {}
    for item in kwargs:
        post.update({item: kwargs.get(item)})
    return mongo_collection.insert_one(post)
