from fastapi import APIRouter
from config.db import resource_collection
from models.model import Resources
from schemas.users import get_resources

resourceRouter = APIRouter()

@resourceRouter.get('/getResource')
async def fetch_resource():
    return get_resources(resource_collection.find())

@resourceRouter.post('/insertResource')
async def insert_resource(resource : Resources):
    resource_collection.insert_one(dict(resource))
    return "Inserted data successfully"