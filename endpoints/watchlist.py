from fastapi import APIRouter, Request
from pydantic import BaseModel
from models.watchlist_model import add_watchlist, fetch_watchlist


router = APIRouter(
    prefix="/api/v1",
    tags=["watchliist"],
    responses={404: {"description": "Not found"}},
)

class create_watchlist(BaseModel):
    user_id: int
    symbol_name: str                     

@router.post("/watchlist")
async def create_watchlist(request:Request,payload:create_watchlist):
    payload = payload.dict()
    response = {"data":await add_watchlist(**payload)}
    return response


@router.get("/watchlist/user/{user_id}")
async def get_all_watchlist(request:Request,user_id:int):
    # print(fetch_instrument_all())
    response = {"data":await fetch_watchlist(user_id)}
    # print(response)
    return response
