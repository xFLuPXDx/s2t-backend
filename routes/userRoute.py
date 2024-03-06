import string
from typing import Annotated
from bson import ObjectId
from fastapi import APIRouter, Depends
from config.db import user_collection 
from schemas.users import get_users
from auth import TokenData, get_current_active_user
from pydantic import BaseModel
from auth import get_password_hash , verify_password

userRouter = APIRouter()

class Update_User_Model(BaseModel):
    user_Fname : str
    user_Lname : str



class Update_Password_Model(BaseModel):
    old_password : str 
    new_password : str


@userRouter.get('/user/get')
async def fetch_users(current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    return user_collection.find_one({"user_Email" : current_user.user_Email},{"_id" : 0 , "user_Fname" : 1 ,"user_Lname" : 1 , "user_Email" : 1 , "user_Type" : 1})


@userRouter.put('/user/update/name')
async def update_users(data : Update_User_Model , current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    ## user = user_collection.find_one({"user_Email" : current_user} , {"_id" : 0 , "user_Fname" : 1 , "user_Lname" : 1 , "user_Email" : 1})
    user_collection.find_one_and_update({ "user_Email" : current_user.user_Email },{"$set" : {"user_Fname" : data.user_Fname , "user_Lname" : data.user_Lname }})

    return True


@userRouter.put('/user/update/password')
async def update_pwd_users(data : Update_Password_Model , current_user: Annotated[TokenData, Depends(get_current_active_user)]):
    pwd = user_collection.find_one({ "user_Email" : current_user.user_Email } , {"hashed_password" : 1 , "_id" : 0} ) 
    if pwd:
        if verify_password(data.old_password , pwd["hashed_password"]):
            user_collection.find_one_and_update({ "user_Email" : current_user.user_Email },{"$set" : { "hashed_password" : get_password_hash(data.new_password)}})
            return "Password Updated"
    return "Wrong Password"