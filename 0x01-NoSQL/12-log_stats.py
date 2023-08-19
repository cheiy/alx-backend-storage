#!/usr/bin/env python3
"""
Script provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs = client.logs.nginx

    print("{} logs".format(nginx_logs.count_documents({})))
    GET = nginx_logs.count_documents({"method": "GET"})
    POST = nginx_logs.count_documents({"method": "POST"})
    PUT = nginx_logs.count_documents({"method": "PUT"})
    PATCH = nginx_logs.count_documents({"method": "PATCH"})
    DELETE = nginx_logs.count_documents({"method": "DELETE"})
    print("Methods:")
    print("\tmethod GET: {}".format(GET))
    print("\tmethod POST: {}".format(POST))
    print("\tmethod PUT: {}".format(PUT))
    print("\tmethod PATCH: {}".format(PATCH))
    print("\tmethod DELETE: {}".format(DELETE))
    GET_PATH = nginx_logs.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(GET_PATH))
