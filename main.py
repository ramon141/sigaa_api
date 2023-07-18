from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from extract import *
import os
from typing import Annotated
import extract
import json


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


def validate_header(request: Request):
    token = request.headers.get('Authorization')

    if token == None or len(token) == 0:
        return False, "Token not found"
    
    if not token.startswith("Bearer "):
        return False, "Token must start with Bearer"
    
    if token != 'Bearer f80a45c9-7c01-4afb-b387-81517c478430':
        return False, "Token invalid"


    api_key = request.headers.get('x-api-key')

    if  api_key == None or len(api_key) == 0:
        return False, "API key not informed"

    return True, ""


@app.get('/unidade/v1/unidades')
def get_units(request: Request):
    ok, message = validate_header(request)
    if not ok:
        raise HTTPException(status_code=400, detail=message)

    with open('contents/unities.json') as json_file:
        data = json.load(json_file)
        return data
    

@app.get('/docente/v1/docentes')
def get_teachers(request: Request):
    ok, message = validate_header(request)
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    
    with open('contents/teachers.json') as json_file:
        data = json.load(json_file)
        return data
    
@app.get('/curso/v1/cursos')
def get_courses(request: Request):
    ok, message = validate_header(request)
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    with open('contents/courses.json') as json_file:
        data = json.load(json_file)
        return data
    
@app.get('/turma/v1/turmas')
def get_turmas(request: Request):
    ok, message = validate_header(request)
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    with open('contents/turmas.json') as json_file:
        data = json.load(json_file)
        return data
    
@app.get('/curso/v1/componentes-curriculares')
def get_componentes_curriculares(request: Request):
    ok, message = validate_header(request)
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    with open('contents/componentes_curriculares.json') as json_file:
        data = json.load(json_file)
        return data
    