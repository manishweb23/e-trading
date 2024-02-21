from fastapi import APIRouter, Request, HTTPException, status  
from pydantic import BaseModel
from typing import Optional
from utils import md5_hash, create_token
from models.user_model import create_user, fetch_user, fetch_user_login
import jwt
import config
import time


router = APIRouter(
    prefix="/api/v1",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

class user(BaseModel):
    name: str
    mobile: str
    password: Optional[str] = None


@router.post("/user")
async def new_user(request:Request,payload:user):
    payload = payload.dict()
    response = await create_user(**payload)
    return {"data":response}


@router.post("/user/login")
async def get_user_login(request:Request, payload: user):
    payload = payload.dict()
    try:
        response = await fetch_user_login(payload['mobile'], md5_hash(payload['password']))
        response = response.__dict__

        if response['is_active'] == False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is inactive!")

        token = await create_token(**response)
        response = {
            "user_id":response['id'],
            "name":response['name'],
            "token":token,
            "next":'/dashboard'
        }
        return {"data":response}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalide Credetials!")


@router.get("/user/{id}")
async def get_user(request:Request,id:int):
    response = await fetch_user(id)
    response = response.__dict__
    del response['password']
    return {"data":response}

