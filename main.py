from fastapi import FastAPI, Query, Request, HTTPException, Form, Depends
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from extract import *
import os
from typing import List
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
    client_id: str
    client_secret: str
    grant_type: str


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


@form_body
class Item(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str
    

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
    
    if token != 'Bearer 7de913d7-1e3b-4eef-bd17-889fb39611e4':
        return False, "Token invalid"


    api_key = request.headers.get('x-api-key')

    if  api_key == None or len(api_key) == 0:
        return False, "API key not informed"

    return True, ""


@app.post('/authz-server/oauth/token')
def get_units(item: Item = Depends(Item)):

    if item.client_id != "piape-vania-id" or item.client_secret != "segredo" or item.grant_type != "client_credentials":
        raise HTTPException(status_code=401, detail="Bad Credentials")

    response = {"access_token":"7de913d7-1e3b-4eef-bd17-889fb39611e4","token_type":"bearer","expires_in":5629071,"scope":"read"}
    return response


@app.get('/unidade/v1/unidades')
def get_units(request: Request):
    ok, message = validate_header(request)
    if not ok:
        raise HTTPException(status_code=401, detail=message)

    with open('contents/unities.json') as json_file:
        data = json.load(json_file)
        return data
    

@app.get('/docente/v1/docentes')
def get_teachers(request: Request):
    ok, message = validate_header(request)
    if not ok:
        raise HTTPException(status_code=401, detail=message)
    
    with open('contents/teachers.json') as json_file:
        data = json.load(json_file)
        return data
    
@app.get('/curso/v1/cursos')
def get_courses(request: Request):
    ok, message = validate_header(request)
    if not ok:
        raise HTTPException(status_code=401, detail=message)
    with open('contents/courses.json') as json_file:
        data = json.load(json_file)
        return data
    
@app.get('/turma/v1/turmas')
def get_turmas(request: Request):
    ok, message = validate_header(request)
    if not ok:
        raise HTTPException(status_code=401, detail=message)
    with open('contents/turmas.json') as json_file:
        data = json.load(json_file)
        return data
    
@app.get('/curso/v1/componentes-curriculares')
def get_componentes_curriculares(request: Request):
    ok, message = validate_header(request)
    if not ok:
        raise HTTPException(status_code=401, detail=message)
    with open('contents/componentes_curriculares.json') as json_file:
        data = json.load(json_file)
        return data
    
@app.get('/usuario/v1/usuarios')
def get_componentes_curriculares(request: Request, login: str = None, id_institucional: List[int] = Query(None, alias='id-institucional')):
    ok, message = validate_header(request)
    if not ok:
        raise HTTPException(status_code=401, detail=message)
    
    with open('contents/usuarios.json') as json_file:
        response = json.load(json_file)

        if login is not None:
            response = [p for p in response if p["login"] == login]

        if id_institucional:
            response = [p for p in response if p["id-institucional"] in id_institucional]

        return response

    