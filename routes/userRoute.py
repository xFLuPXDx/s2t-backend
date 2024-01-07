from bson import ObjectId
from fastapi import APIRouter
from config.db import user_collection 
from models.model import Users 
from schemas.users import get_users
from auth import get_current_active_user

userRouter = APIRouter()

@userRouter.get('/getUsers')
async def fetch_users():
    return get_users(user_collection.find())

@userRouter.post('/insertUser')
async def insert_user(user : Users):
    user_collection.insert_one(dict(user))
    return "Inserted data successfully"

@userRouter.put('/updateUser/')
async def update_user(id : str , user : Users):
    user_collection.find_one_and_update({"user_Id" : id},{"$set":dict(user)})


    