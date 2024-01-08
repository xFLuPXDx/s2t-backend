from typing import Annotated
from fastapi import APIRouter, Depends
from auth import TokenData, get_current_active_user
from config.db import group_collection , user_collection
from models.model import  Groups
from schemas.users import get_groups , get_group, get_user 

groupRouter = APIRouter()

@groupRouter.post('/insertGroup')
async def insert_group(group : Groups , current_user: Annotated[TokenData, Depends(get_current_active_user)]):
    user_cursor = get_user(user_collection.find_one({ 'user_Email' : current_user.user_Email}))
    if user_cursor["user_Type"] == "educator" :
        group_collection.insert_one(dict(group))
        return True
    
    return False

@groupRouter.get('/fetchGroups')
async def fetch_group(current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    user_cursor = get_user(user_collection.find_one({ 'user_Email' : current_user.user_Email}))
    groupIds = user_cursor["group_Ids"]

    grps = list()

    if groupIds != [] :
        for code in groupIds :
            grps.append(get_group(group_collection.find_one({"group_Id" : code})))
            
        return grps
    return False


@groupRouter.post('/joinGroup')
async def join_group(code : str , current_user: Annotated[TokenData, Depends(get_current_active_user)]):
    user_collection.find_one_and_update({'user_Email' : current_user.user_Email},{"$push" : { "group_Ids" : code }})
    user_cursor = get_user(user_collection.find_one({ 'user_Email' : current_user.user_Email}))
    if user_cursor["user_Type"] == "educator" : 
        group_collection.find_one_and_update({'group_Id' : code},{"$push" : {"educator_Ids" : user_cursor["user_Id"]}})
    else:
        group_collection.find_one_and_update({'group_Id' : code},{"$push" : {"learner_Ids" : user_cursor["user_Id"]}})
    return True


@groupRouter.get('/userInGroups')
async def user_In_group( code : str , current_user : Annotated[TokenData, Depends(get_current_active_user)]):
    
    group = get_group(group_collection.find({"group_Id" : code}))
    educator_Ids = group["educator_Ids"]
    learner_Ids = group["learner_Ids"]




