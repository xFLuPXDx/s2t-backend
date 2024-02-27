import secrets
import string
from typing import Annotated
from fastapi import APIRouter, Depends
from auth import TokenData, get_current_active_user
from config.db import group_collection , user_collection
from models.model import  Groups_Model , Code
from schemas.users import  get_groups
from S2T.speechtotext import s2tConvert

groupRouter = APIRouter()

@groupRouter.get('/getGroup')
async def getGroup():
    return get_groups(group_collection.find())

@groupRouter.post('/group/peoples/learners')
async def get_peoples(code : Code , current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    dc = dict(code)

    learners_in_groups = group_collection.find_one({"group_Id" : dc["group_Id"]} , {"_id" : 0 , "learner_Ids" : 1  })
    print(learners_in_groups)
    learners = list()
    
    if learners_in_groups["learner_Ids"] != [] :
        for code in learners_in_groups["learner_Ids"] :
            learners.append(user_collection.find_one({"user_Id" : code} , {"_id" : 0 , "user_Fname" : 1 , "user_Lname" : 1}))             
        return learners
    

    return []

@groupRouter.post('/group/peoples/educators')

async def get_peoples(code : Code , current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    dc = dict(code)

    educators_in_groups = group_collection.find_one({"group_Id" : dc["group_Id"]} , {"_id" : 0 , "educator_Ids" : 1 })

    educators = list()
    
    if educators_in_groups["educator_Ids"] != [] :
        for code in educators_in_groups["educator_Ids"] :
            educators.append(user_collection.find_one({"user_Id" : code} , {"_id" : 0 , "user_Fname" : 1 , "user_Lname" : 1}))             
        return educators
    

    return []


@groupRouter.post('/group/delete')
async def delete_group(code : Code , current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    dc = dict(code)

    user_cursor = user_collection.find_one({ 'user_Email' : current_user.user_Email} , {"_id" : 0 ,"user_Id" : 1 , "user_Type" : 1})

    user_collection.find_one_and_update({'user_Email' : current_user.user_Email},{"$pull" : { "group_Ids" :  dc["group_Id"] }})
    
    if user_cursor["user_Type"] == "educator" : 
        group_collection.find_one_and_update({'group_Id' : dc["group_Id"]},{"$pull" : {"educator_Ids" : user_cursor["user_Id"]}})
    else:
        group_collection.find_one_and_update({'group_Id' :  dc["group_Id"]},{"$pull" : {"learner_Ids" : user_cursor["user_Id"]}})
    return True


@groupRouter.post('/group/insert')
async def insert_group(group : Groups_Model , current_user: Annotated[TokenData, Depends(get_current_active_user)]):
    
    user_cursor = user_collection.find_one({'user_Email' : current_user.user_Email} , {"user_Type" : 1 , "_id" : 0 , "user_Id" : 1})

    new_group = dict(group)
    new_group["educator_Ids"].append(user_cursor["user_Id"])
    
    if user_cursor["user_Type"] == "educator" :
        while True:
            code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
            if not(group_collection.find_one({"group_Id" : code})):
                new_group["group_Id"] = code
                break

        group_collection.insert_one(new_group)
        user_collection.find_one_and_update({'user_Email' : current_user.user_Email},{"$push" : { "group_Ids" :  new_group["group_Id"] }})
        return True
    
    return False

@groupRouter.get('/group/fetch')
async def fetch_group(current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    user_cursor = user_collection.find_one({ 'user_Email' : current_user.user_Email} , {"_id" : 0 , "group_Ids" : 1 })

    grps = list()
    
    if user_cursor["group_Ids"] != [] :
        for code in user_cursor["group_Ids"] :
            grps.append(group_collection.find_one({"group_Id" : code} , {"_id" : 0 ,"group_Id" : 1, "group_Name" : 1 , "group_Subject" : 1 }))              
        return grps
    
    return []


@groupRouter.post('/group/join')
async def join_group(code : Code , current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    dc = dict(code)
    user_cursor = user_collection.find_one({ 'user_Email' : current_user.user_Email} , {"_id" : 0 ,"user_Id" : 1 , "group_Ids" : 1 , "user_Type" : 1})

    if dc["group_Id"] in user_cursor["group_Ids"]:
        return "already joined"

    if user_cursor["user_Type"] == "educator" : 
        group_collection.find_one_and_update({'group_Id' : dc["group_Id"]},{"$push" : {"educator_Ids" : user_cursor["user_Id"]}})
    else:
        group_collection.find_one_and_update({'group_Id' : dc["group_Id"]},{"$push" : {"learner_Ids" : user_cursor["user_Id"]}})

    user_collection.find_one_and_update({'user_Email' : current_user.user_Email},{"$push" : { "group_Ids" : dc["group_Id"] }})
    return True


@groupRouter.post('/group/users')
async def user_In_group( code : Code , current_user : Annotated[TokenData, Depends(get_current_active_user)]):
    
    dc = dict(code)

    group = group_collection.find_one({"group_Id" : dc["group_Id"]} , {"_id" : 0 , "educator_Ids" : 1 , "learner_Ids" : 1})
    educator_Ids = group["educator_Ids"]
    learner_Ids = group["learner_Ids"]

    users_in_group = list()

    for id in educator_Ids:
        users_in_group.append(user_collection.find_one({"user_Id" : id} , {"_id" : 0 , "user_Id" : 1 , "user_Fname" : 1 , "user_Lname" : 1}))

    for id in learner_Ids:
        users_in_group.append(user_collection.find_one({"user_Id" : id} , {"_id" : 0 , "user_Id" : 1 , "user_Fname" : 1 , "user_Lname" : 1}))
    
    return users_in_group


@groupRouter.post('/group/s2t')
async def s2tCon():
    return s2tConvert()