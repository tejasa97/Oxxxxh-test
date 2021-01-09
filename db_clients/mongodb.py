from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL", "localhost")


class MongoConnection():

    def __init__(self, database='mongolog'):
        client = MongoClient(MONGO_URL)
        self.database_name = database

        self.db = client[self.database_name]

    def get_collection(self, name):
        return self.db[name]
