from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from models.transaction_model import create_transaction, fetch_transaction, fetch_balance, fetch_pl

router = APIRouter(
    prefix="/api/v1",
    tags=["transaction"],
    responses={404: {"description": "Not found"}},
)

class transaction(BaseModel):
    user_id:int
    amount:float
    for_id:Optional[int]=None
    transaction_for:str
    transaction_type:str


@router.post("/transaction/addbalance")
async def new_transaction(request:Request,payload:transaction):
    payload = payload.dict()
    # payload['created_by'] = request.state.user_id
    response = await create_transaction(**payload)
    return {"data":response}


@router.get("/transaction/user/{user_id}")
async def get_user_transaction(request:Request,user_id:int):
    response = await fetch_transaction(user_id)
    return {"data":response}


@router.get("/transaction/user/{user_id}/balance")
async def get_user_balance(request:Request,user_id:int):
    response = await fetch_balance(user_id)
    return {"data":{"balance":response}}


@router.get("/transaction/user/{user_id}/pl")
async def get_user_pl(request:Request,user_id:int):
    response = await fetch_pl(user_id)
    return {"data":{"balance":response}}