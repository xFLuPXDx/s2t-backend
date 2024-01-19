def get_single_user(user) -> dict:
    return{
        "_id" : str(user["_id"]) ,
        "user_Id" : user["user_Id"],
        "user_Fname" : user["user_Fname"],
        "user_Lname" : user["user_Lname"],
        "user_Email" : user["user_Email"],
        "user_Type" : user["user_Type"],
        "hashed_password" : user["hashed_password"],
       "group_Ids" : user["group_Ids"],
        
    }

def get_users(users) -> list:
    return [
        get_single_user(user) for user in users
    ]

def get_group(group) -> dict:
    return {
        "_id" : str(group["_id"]) ,
        "group_Id" : group["group_Id"],
        "group_Name" : group["group_Name"],
        "group_Subject" : group["group_Subject"],
        "educator_Ids" : group["educator_Ids"],
        "learner_Ids" : group["learner_Ids"],
        "resource_Ids" : group["resource_Ids"],
    }

def get_groups(groups) -> list:
    return [
        get_group(group) for group in groups
    ]

def get_resource(resource) -> dict:
    return {
        "_id" : str(resource["_id"]) ,
        "resource_Id" : resource["resource_Id"],
        "lecture_Transcript" : resource["lecture_Transcript"],
        "summarized_Text" : resource["summarized_Text"],
        "resource_links" : resource["resource_links"],
    }

def get_resources(resources) -> list:
    return [
        get_resource(resource) for resource in resources
    ]

def get_user_Ids(iDs) -> dict :
    return {
        "educator_Ids" : iDs["educator_Ids"],
        "learner_Ids" : iDs["learner_Ids"],
    }