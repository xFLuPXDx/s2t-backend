from pymongo import MongoClient

conn = MongoClient("mongodb+srv://rohit:12345@fastapi.e2rnzdr.mongodb.net/")

db = conn.Users

user_collection = db["user_collection"]
group_collection = db["group_collection"]
resource_collection = db["resource_collection"]