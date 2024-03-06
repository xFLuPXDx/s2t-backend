from fastapi import APIRouter,File,UploadFile
from S2T.speechtotext import s2tConvert
from config.db import resource_collection
from models.model import Resources_Model
from schemas.users import get_resources
import uuid
import magic
import boto3

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
tmp = "S2T/temp"
@resourceRouter.post('/resource/upload')
async def upload_file(file:UploadFile = File(...)):
    contents = await file.read()
    file_type = magic.from_buffer(buffer=contents , mime=True)
    file.filename = f"{uuid.uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}"
    with open(f"{tmp}{file.filename}","wb") as f:
        f.write(contents)
    summarry = s2tConvert(f"{tmp}{file.filename}")
    s3.upload_file(f"{tmp}{file.filename}","clarity",file.filename)
    
    return {"Filename " : file.filename , "summarry" : summarry}
