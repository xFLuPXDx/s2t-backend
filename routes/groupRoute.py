import secrets
import string
from typing import Annotated
from fastapi import APIRouter, Depends
from auth import TokenData, get_current_active_user
from config.db import group_collection , user_collection
from models.model import  Groups_Model
from schemas.users import  get_group, get_user

groupRouter = APIRouter()

@groupRouter.post('/group/insert')
async def insert_group(group : Groups_Model , current_user: Annotated[TokenData, Depends(get_current_active_user)]):
    
    user_cursor = user_collection.find_one({'user_Email' : current_user.user_Email} , {"user_Type" : 1 , "_id" : 0} )

    new_group = dict(group)

    if user_cursor["user_Type"] == "educator" :
        while True:
            code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
            if not(group_collection.find_one({"group_Id" : code})):
                new_group["group_Id"] = code
                break

        group_collection.insert_one(new_group)
        return True
    
    return False

    """ user_cursor = get_user(user_collection.find_one({ 'user_Email' : current_user.user_Email}))
    new_group = dict(group)

    set_codes = set()

    while True:
        code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
        if code not in set_codes:
            new_group["group_Id"] = code
            break

    if user_cursor["user_Type"] == "educator" :
        group_collection.insert_one(new_group)
        return True
    
    return False """

@groupRouter.get('/group/fetch')
async def fetch_group(current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    user_cursor = user_collection.find_one({ 'user_Email' : current_user.user_Email} , {"_id" : 0 , "group_Ids" : 1 })

    grps = list()

    if user_cursor["group_Ids"] != [] :
        for code in user_cursor["group_Ids"] :
            grps.append(get_group(group_collection.find_one({"group_Id" : code})))            
        return grps
    
    return False


@groupRouter.post('/group/join')
async def join_group(code : str , current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    user_cursor = user_collection.find_one({ 'user_Email' : current_user.user_Email} , {"_id" : 0 ,"user_Id" : 1 , "group_Ids" : 1 , "user_Type" : 1})

    if code in user_cursor["group_Ids"]:
        return "already joined"

    if user_cursor["user_Type"] == "educator" : 
        group_collection.find_one_and_update({'group_Id' : code},{"$push" : {"educator_Ids" : user_cursor["user_Id"]}})
    else:
        group_collection.find_one_and_update({'group_Id' : code},{"$push" : {"learner_Ids" : user_cursor["user_Id"]}})

    user_collection.find_one_and_update({'user_Email' : current_user.user_Email},{"$push" : { "group_Ids" : code }})
    return True


@groupRouter.get('/group/users')
async def user_In_group( code : str , current_user : Annotated[TokenData, Depends(get_current_active_user)]):
    
    group = group_collection.find_one({"group_Id" : code} , {"_id" : 0 , "educator_Ids" : 1 , "learner_Ids" : 1})
    educator_Ids = group["educator_Ids"]
    learner_Ids = group["learner_Ids"]

    users_in_group = list()

    for id in educator_Ids:
        users_in_group.append(user_collection.find_one({"user_Id" : id} , {"_id" : 0 , "user_Id" : 1 , "user_Fname" : 1 , "user_Lname" : 1}))

    for id in learner_Ids:
        users_in_group.append(user_collection.find_one({"user_Id" : id} , {"_id" : 0 , "user_Id" : 1 , "user_Fname" : 1 , "user_Lname" : 1}))
    
    return users_in_group


