from typing import Annotated
from bson import ObjectId
from fastapi import APIRouter, Depends
from config.db import user_collection 
from models.model import Users 
from schemas.users import get_users
from auth import TokenData, get_current_active_user

userRouter = APIRouter()

@userRouter.get('/getUsers')
async def fetch_users(current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    return get_users(user_collection.find())




    