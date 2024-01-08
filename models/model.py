from pydantic import BaseModel

class Users(BaseModel):
    user_Id : str
    user_Fname : str
    user_Lname : str
    user_Email : str
    group_Ids : list | None = []
    user_Type : str
    hashed_password : str
    
class Groups(BaseModel):
    group_Id : str
    group_Name : str
    group_Subject : str
    educator_Ids : list | None = []
    learner_Ids : list | None = []

class Resources(BaseModel):
    resource_Id : str
    lecture_Transcript : str
    summarized_Text  : str
    resource_links : list | None = []