from pydantic import BaseModel

class Users_Model(BaseModel):
    user_Id : str
    user_Fname : str
    user_Lname : str
    user_Email : str
    group_Ids : list | None = []
    user_Type : str
    hashed_password : str
    
class Groups_Model(BaseModel):
    group_Id : str
    group_Name : str
    group_Subject : str
    educator_Ids : list | None = []
    learner_Ids : list | None = []
    resource_Ids : list | None = []

class Resources_Model(BaseModel):
    resource_Id : str
    time_Stamp : str
    summarized_Text  : str
    topics_Covered  : list | None = []
    resource_links : list | None = []

class Code(BaseModel):
     group_Id : str