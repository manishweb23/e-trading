from fastapi import APIRouter, Request
from models.order_model import fetch_instrument_all,filter_instrument, filter_instrument_expiry, filter_instrument_name, filter_instrument_all
from utils import create_instruments


router = APIRouter(
    prefix="/api/v1",
    tags=["instruments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/instrument/all/type/{instrument_type}")
async def get_all_instrument(request:Request,instrument_type:str):
    # print(fetch_instrument_all())
    response = {"data":await fetch_instrument_all(instrument_type)}
    # print(response)
    return response

@router.get("/instrument/expiry/symbol/{symbol}")
async def get_expiry_date_instrument(request:Request,symbol:str):
    response = {"data": {"expiry":await filter_instrument_expiry(symbol)}}
    return response

@router.get("/instrument/symbol/{symbol}/expiry/{expiry}")
async def get_all_instrument(request:Request,symbol:str,expiry:str):
    response = {"data":await filter_instrument(symbol,expiry)}
    return response


@router.get("/instrument/name/{name}")
async def get_all_instrument_name(request:Request,name:str):
    response = {"data":await filter_instrument_name(name)}
    return response

@router.get("/instrument/all/limit/{limit}/offset/{offset}")
async def get_all_instrument(request:Request,limit:int,offset:int):
    response = {"data":await filter_instrument_all(limit,offset)}
    return response


