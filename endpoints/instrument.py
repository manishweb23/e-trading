from fastapi import APIRouter, Request
from models.order_model import fetch_instrument_all,filter_instrument
from utils import create_instruments


router = APIRouter(
    prefix="/api/v1",
    tags=["instruments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/instrument/all/{instrument_type}")
async def get_all_instrument(request:Request,instrument_type:str):
    # print(fetch_instrument_all())
    response = {"data":await fetch_instrument_all(instrument_type)}
    # print(response)
    return response


@router.get("/instrument/{symbol}")
async def get_all_instrument(request:Request,symbol:str):
    response = {"data":await filter_instrument(symbol)}
    return response


