from fastapi import FastAPI
from routes.groupRoute import groupRouter
from routes.resourceRoute import resourceRouter
from routes.userRoute import userRouter
from auth import authRouter
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI()

app.include_router(groupRouter)
app.include_router(resourceRouter)
app.include_router(userRouter)
app.include_router(authRouter)



app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

print("ndkjasjkdbc")