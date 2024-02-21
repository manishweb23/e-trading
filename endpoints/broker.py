from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from utils import md5_hash
from models.broker_model import create_token, fetch_token

router = APIRouter(
    prefix="/api/v1",
    tags=["broker"],
    responses={404: {"description": "Not found"}},
)

class token(BaseModel):
    code: Optional[str] = None
    token: Optional[str] = None


@router.post("/broker")
async def new_user(request:Request,payload:token):
    payload = payload.dict()
    response = await create_token(**payload)
    return {"data":response}


@router.get("/broker/latest")
async def get_user(request:Request,id:int):
    response = await fetch_token()
    return {"data":response}

