from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")

MONGO_URL = config['MONGO_URL']
conn = MongoClient(MONGO_URL)

db = conn.Users

user_collection = db["user_collection"]
group_collection = db["group_collection"]
resource_collection = db["resource_collection"]