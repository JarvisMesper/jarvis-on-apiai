import os

from pymongo import MongoClient


class DBClient:

    def get_db():
        mongodb_host = os.environ.get('MONGODB_HOST')
        client = MongoClient(mongodb_host)
        db = client.jarvis
        return db
