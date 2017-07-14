from pymongo import MongoClient

class DBClient:

    def get_db():
        client = MongoClient("mongodb://localhost:27017")
        db = client.jarvis
        return db