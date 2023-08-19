#!/usr/bin/env python3
"""
Module contains function that changes all topics of a school document
"""


def update_topics(mongo_collection, name, topics):
    """
    Function changes all topics of a school document based on the name
    """
    mongo_collection.update_one({"name": name},
                                {"$push": {"topics":
                                           {"$each": topics}}})
