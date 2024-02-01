from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from models.limit_model import create_limit, update_limit, fetch_limit



class limit(BaseModel):
    user_id: int
    amount: Optional[float] = None


router = APIRouter(
    prefix="/api/v1",
    tags=["limit"],
    responses={404: {"description": "Not found"}},
)


@router.post("/limit")
async def add_limit(request:Request,payload:limit):
    payload = payload.dict()
    response = await create_limit(**payload)
    return response

@router.put("/limit/{limit_id}")
async def change_limit(request:Request,payload:limit,limit_id:int):
    response = await update_limit(limit_id,**payload)
    return response

@router.get("/limit/user_id/{user_id}")
async def get_limit(request:Request,user_id:int):
    response = await fetch_limit(user_id)
    return response 

