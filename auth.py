from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from config.db import user_collection 
from models.model import Users

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "7fc88d2a3526c846b443209e25fce190729f3b66c4ed1d94ce84f0b33599caf7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

authRouter = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_Email : str | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

#works
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#works
def get_password_hash(password):
    return pwd_context.hash(password)

#works
def get_user(email: str):
    return user_collection.find_one({"user_Email" : email})

#works
def authenticate_user( email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

#works
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#works
@authRouter.post("/auth", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["user_Email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


#works
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(user_Email = email)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.user_Email)
    if user is None:
        raise credentials_exception
    return token_data


#works
async def get_current_active_user(
    current_user: Annotated[str, Depends(get_current_user)]
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

#works
@authRouter.get("/users/me/")
async def read_users_me(
    current_user: Annotated[str, Depends(get_current_active_user)]
):
    return current_user

#works
@authRouter.post("/signUp")
async def signUp( user : Users):

    res = dict(user)

    user_collection.insert_one(
        {
            "user_Id" : res["user_Id"],
            "user_Fname" : res["user_Fname"],
            "user_Lname" : res["user_Lname"],
            "user_Email" : res["user_Email"],
            "group_Ids" : res["group_Ids"],
            "user_Type" : res["user_Type"],
            "hashed_password" : get_password_hash(res["hashed_password"]),
        }
    )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": res["user_Email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}