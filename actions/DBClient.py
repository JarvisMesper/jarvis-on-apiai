from pymongo import MongoClient
import os

class DBClient:

    def get_db():
        MONGODB_HOST=os.environ.get('MONGODB_HOST')
        client = MongoClient(MONGODB_HOST)
        db = client.jarvis
        return db