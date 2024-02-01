from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from utils import md5_hash
from models.user_model import create_user, fetch_user

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


@router.get("/user/{id}")
async def get_user(request:Request,id:int):
    response = await fetch_user(id)
    # response.pop('password')
    response = response.__dict__
    del response['password']
    return {"data":response}

