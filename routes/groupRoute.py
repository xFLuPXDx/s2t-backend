from typing import Annotated
from fastapi import APIRouter, Depends
from auth import TokenData, get_current_active_user
from config.db import group_collection , user_collection
from models.model import  Groups, Users 
from schemas.users import get_groups , get_group, get_user 

groupRouter = APIRouter()

@groupRouter.get('/getGroup')
async def fetch_group(current_user: Annotated[TokenData, Depends(get_current_active_user)]):
    cursor = get_user( user_collection.find_one({ 'user_Email' : current_user.user_Email}))
    groupIds = cursor["group_Ids"]
    return groupIds


@groupRouter.post('/insertGroup')
async def insert_group(group : Groups , current_user: Annotated[TokenData, Depends(get_current_active_user)]):
    group_collection.insert_one(dict(group))
    return "Inserted data successfully"

@groupRouter.get('/getSpecific_Group/{gid}')
def getSpecific_Group(gid : str):
    return get_group(group_collection.find_one({'group_Id' : gid}))





