#!/usr/bin/env python3
"""
This module contains a function that lists all documents in a collection
"""


def list_all(mongo_collection):
    """
    Function lists all documents in a collection
    """
    return mongo_collection.find()
