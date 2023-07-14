from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from extract import *
import os
import extract


SECRET = os.getenv("SECRET")

#
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Msg(BaseModel):
    msg: str
    secret: str

class Credentials(BaseModel):
    username: str
    password: str

@app.get("/")

async def root():
    return {
        'message': 'Acesse a página /docs'
    }


@app.post('/login')
def get_user(credentials: Credentials):
    driver = extract.createDriver()
    user = extract.get_user(driver, credentials.username, credentials.password)
    driver.quit()
    return user
    