import secrets
import string
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException , status
from auth import TokenData, get_current_active_user
from config.db import group_collection , user_collection
from models.model import Groups_Model , Code
from schemas.users import get_groups

groupRouter = APIRouter()

@groupRouter.get('/getGroup')
async def getGroup():
    return get_groups(group_collection.find())

@groupRouter.post('/group/peoples/learners')
async def get_peoples(code : Code , current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    dc = dict(code)

    learners_in_groups = group_collection.find_one({"group_Id" : dc["group_Id"]} , {"_id" : 0 , "learner_Ids" : 1  })

    lrs = dict()
    learnerslist = list()
    
    if learners_in_groups["learner_Ids"] != [] :
        for code in learners_in_groups["learner_Ids"] :
            learnerslist.append(user_collection.find_one({"user_Id" : code} , {"_id" : 0 , "user_Fname" : 1 , "user_Lname" : 1}))           
        lrs.update({
            "count" : len(learnerslist),
            "result" : learnerslist
        })         
        return lrs
    

    return []

@groupRouter.post('/group/peoples/educators')

async def get_peoples(code : Code , current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    dc = dict(code)

    educators_in_groups = group_collection.find_one({"group_Id" : dc["group_Id"]} , {"_id" : 0 , "educator_Ids" : 1 })
    eds = dict()
    educatorslist = list()
    
    if educators_in_groups["educator_Ids"] != [] :
        for code in educators_in_groups["educator_Ids"] :
            educatorslist.append(user_collection.find_one({"user_Id" : code} , {"_id" : 0 , "user_Fname" : 1 , "user_Lname" : 1}))    
        eds.update({
            "count" : len(educatorslist),
            "result" : educatorslist
        })         
        return eds
    

    return []


@groupRouter.post('/group/delete')
async def delete_group(code : Code , current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    dc = dict(code)

    user_cursor = user_collection.find_one({ 'user_Email' : current_user.user_Email} , {"_id" : 0 ,"user_Id" : 1 , "user_Type" : 1})

    user_collection.find_one_and_update({'user_Email' : current_user.user_Email},{"$pull" : { "group_Ids" :  dc["group_Id"] }})
    
    if user_cursor["user_Type"] == "educator" : 
        group_collection.find_one_and_update({'group_Id' : dc["group_Id"]},{"$pull" : {"educator_Ids" : user_cursor["user_Id"]}})
        return True
    else:
        group_collection.find_one_and_update({'group_Id' :  dc["group_Id"]},{"$pull" : {"learner_Ids" : user_cursor["user_Id"]}})
        return True
    
    return False


@groupRouter.post('/group/create')
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

    grps = dict()
    grpslist = list()
    
    if user_cursor["group_Ids"] != [] :
        for code in user_cursor["group_Ids"] :
            grpslist.append(group_collection.find_one({"group_Id" : code} , {"_id" : 0 ,"group_Id" : 1, "group_Name" : 1 , "group_Subject" : 1 }))              
        
        grps.update({"count" : len(grpslist) , "result" : grpslist})
        return grps
    
    return []


@groupRouter.post('/group/join')
async def join_group(code : Code , current_user: Annotated[TokenData, Depends(get_current_active_user)]):

    dc = dict(code)
    user_cursor = user_collection.find_one({ 'user_Email' : current_user.user_Email} , {"_id" : 0 ,"user_Id" : 1 , "group_Ids" : 1 , "user_Type" : 1})
    
    if dc["group_Id"] in user_cursor["group_Ids"]:
        return "already joined"

    if group_collection.find_one({"group_Id" : dc["group_Id"]}):
        if user_cursor["user_Type"] == "educator" : 
            group_collection.find_one_and_update({'group_Id' : dc["group_Id"]},{"$push" : {"educator_Ids" : user_cursor["user_Id"]}})
        else:
            group_collection.find_one_and_update({'group_Id' : dc["group_Id"]},{"$push" : {"learner_Ids" : user_cursor["user_Id"]}})

        user_collection.find_one_and_update({'user_Email' : current_user.user_Email},{"$push" : { "group_Ids" : dc["group_Id"] }})
        raise HTTPException(
            status_code=status.HTTP_200_OK,
        )
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Code",
        )


@groupRouter.post('/group/users')
async def user_In_group( code : Code , current_user : Annotated[TokenData, Depends(get_current_active_user)]):
    
    dc = dict(code)

    group = group_collection.find_one({"group_Id" : dc["group_Id"]} , {"_id" : 0 , "educator_Ids" : 1 , "learner_Ids" : 1})
    educator_Ids = group["educator_Ids"]
    learner_Ids = group["learner_Ids"]

    users_in_group = dict()

    elist = list()
    llist = list()

    for id in educator_Ids:
        elist.append(user_collection.find_one({"user_Id" : id} , {"_id" : 0 , "user_Id" : 1 , "user_Fname" : 1 , "user_Lname" : 1}))

    for id in learner_Ids:
        llist.append(user_collection.find_one({"user_Id" : id} , {"_id" : 0 , "user_Id" : 1 , "user_Fname" : 1 , "user_Lname" : 1}))
    
    users_in_group.update({
        "educator_Ids" : { "count" : len(elist) , "result" : elist} ,
        "learner_Ids" : { "count" : len(llist) , "result" : llist},
    })

    return users_in_group

