import time
from fastapi import APIRouter,File,UploadFile
from S2T.speechtotext import s2tConvert
from config.db import resource_collection
from models.model import Resources_Model
from schemas.users import get_resources
import uuid
import magic
import boto3
import os

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

@resourceRouter.post('/resource/upload')
async def upload_file(file:UploadFile = File(...)):

    contents = await file.read()

    file_type = magic.from_buffer(buffer=contents , mime=True)
    file.filename = f"{uuid.uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}"
    with open(f"{tmp}{file.filename}","wb") as f:
        f.write(contents)

    ntype = f"{uuid.uuid4()}.mp3"
    os.system(f"ffmpeg -i {tmp}{file.filename} -c:a libmp3lame {tmp}{ntype}")

    summarry = s2tConvert(f"{tmp}{ntype}")
    s3.upload_file(f"{tmp}{ntype}","clarity",f"{ntype}")
    os.remove(f"{tmp}{ntype}")
    os.remove(f"{tmp}{file.filename}")
    print(summarry)
    return {"Filename " : ntype , "summarry" : summarry}
