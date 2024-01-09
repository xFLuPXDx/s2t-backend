from fastapi import APIRouter
from config.db import resource_collection
from models.model import Resources_Model
from schemas.users import get_resources

resourceRouter = APIRouter()