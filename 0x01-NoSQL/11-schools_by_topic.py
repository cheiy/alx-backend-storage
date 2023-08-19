#!/usr/bin/env python3
"""
Module contains function that returns the list of school
having a specific topi
"""


def schools_by_topic(mongo_collection, topic):
    """
    Function returns a list of schools having the specified topic
    """
    result = mongo_collection.find({"topics": topic})
    return result
