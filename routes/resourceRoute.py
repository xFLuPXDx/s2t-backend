import time
from fastapi import APIRouter,File,UploadFile
from S2T.speechtotext import s2tConvert
from config.db import resource_collection , group_collection
from models.model import Resources_Model , Code
from schemas.users import get_resources
from S2T.youtubeUrlGen import get_youtube_url
import uuid
import magic
import boto3
import os
import datetime

SUPPORTED_FILE_TYPES = {
    'audio/mpeg' : 'mpeg',
    'audio/mp3' : 'mp3',
    'image/png' : 'png',
    'video/3gpp' : '3gpp'
}
s3 = boto3.client(
    service_name='s3',
    aws_access_key_id='zVAt4fWHpjDjr6kA',
    aws_secret_access_key='3wIgvl28dCGyrKkBKdOnigJS4DWsGLu75PhpEGac',
    endpoint_url='https://s3.tebi.io'
)

resourceRouter = APIRouter()
tmp = "S2T/temp/"

@resourceRouter.post('/resource/upload/{gid}')
async def upload_file(gid : str , file:UploadFile = File(...) ):

    contents = await file.read()

    file_type = magic.from_buffer(buffer=contents , mime=True)
    file.filename = f"{uuid.uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}"
    with open(f"{tmp}{file.filename}","wb") as f:
        f.write(contents)

    ntype = f"{uuid.uuid4()}.mp3"
    os.system(f"ffmpeg -i {tmp}{file.filename} -c:a libmp3lame {tmp}{ntype}")

    response = s2tConvert(f"{tmp}{ntype}")
    s3.upload_file(f"{tmp}{ntype}","clarity",f"{ntype}")
    os.remove(f"{tmp}{ntype}")
    os.remove(f"{tmp}{file.filename}")
    
    yt_url_id = list()
    print(response)
    for topic in response['headpoints']:
        yt_url_id.append(get_youtube_url(topic))
    date = datetime.datetime.now()
    resource_collection.insert_one({
        "resource_Id" : ntype,
        "time_Stamp" : str(date.strftime("%d/%m/%Y")),
        "summarized_Text" : response['summary'],
        "topics_Covered"  : response['headpoints'],
        "resource_links" : yt_url_id,
    })
    
    group_collection.find_one_and_update({'group_Id' : gid},{"$push" : { "resource_Ids" :  ntype }})

    return True

@resourceRouter.post('/resource/fetch')
async def fetch_resources(code : Code):

    dc = dict(code)

    user_cursor = group_collection.find_one({'group_Id' : dc["group_Id"]},{"_id" : 0 ,"resource_Ids" : 1})
    
    list_resources = list()
    resources = dict()

    if user_cursor["resource_Ids"] != [] :
        for rid in user_cursor["resource_Ids"] :        
            list_resources.append(resource_collection.find_one({"resource_Id" : rid} , {"_id" : 0 ,"time_Stamp" : 1, "summarized_Text" : 1 ,"topics_Covered" : 1, "resource_links" : 1 }))              
        resources.update({
            "count" : len(list_resources),
            "result" : list_resources
        })
        
        return resources
    
    return []


@resourceRouter.post('/resource/fetch/id')
async def fetch_resources(code : Code):

    dc = dict(code)

    user_cursor = group_collection.find_one({'group_Id' : dc["group_Id"]},{"_id" : 0 ,"resource_Ids" : 1})
    
    list_resources_Id = list()
    resources_Id = dict()

    if user_cursor["resource_Ids"] != [] :
        for rid in user_cursor["resource_Ids"] :        
            list_resources_Id.append(resource_collection.find_one({"resource_Id" : rid} , {"_id" : 0 ,"time_Stamp" : 1, "resource_Id" : 1}))              
        resources_Id.update({
            "count" : len(list_resources_Id),
            "result" : list_resources_Id
        })
        
        return resources_Id
    
    return []