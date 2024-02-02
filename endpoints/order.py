from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
from utils import get_ltp
from models.order_model import open_order, close_order, fetch_all_filtered_orders, fetch_single_orders   
from models.transaction_model import create_transaction
import datetime


router = APIRouter(
    prefix="/api/v1",
    tags=["order"],
    responses={404: {"description": "Not found"}},
)

class filter_order(BaseModel):
    order_id: Optional[int] = None
    user_id: Optional[int] = None
    symbol: list[str]
    exchange: Optional[str] = None
    trade_type: Optional[str] = None
    expiry_date: Optional[str] = None
    open_order: Optional[bool] = None
    close_order: Optional[bool] = None


class order(BaseModel):
    user_id: int
    symbol: Optional[str] = None
    exchange: Optional[str] = None
    trade_type: Optional[str] = None
    expiry_date: Optional[str] = None
    open_price: Optional[float] = None
    close_price: Optional[float] = None
    open_ticker: Optional[float] = None
    close_ticker: Optional[float] = None
    stop_loss: Optional[float] = None
    quantity: Optional[int] = None
    lot_size: Optional[int] = None
    order_time_chart: Optional[str] = None
    open_time: Optional[str] = None
    close_time: Optional[str] = None


@router.post("/order")
async def create_order(request:Request,payload:order):
    payload = payload.dict()
    try:
        ltp_data = await get_ltp(payload['symbol'])
        for k in ltp_data['data'].keys():
            ltp = ltp_data['data'][k]['last_price']
        payload['open_price'] = ltp
        payload['open_time'] = str(datetime.datetime.now())
        response = await open_order(**payload)
        transaction_detail = {
            "amount": ltp * payload['quantity'] * payload['lot_size'],
            "user_id": payload['user_id'],
            "for_id":response,
            "transaction_for":"open_order",
            "transaction_type":"DR",
            # "created_by" :request.state.user_id
        }
        await create_transaction(**transaction_detail)
        return {"data":{"message":"order succesfull", "order_id":response}}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Item not found")


@router.put("/order/{order_id}")
async def update_order(request:Request,payload:order,order_id:int):
    payload = payload.dict()
    try:
        ltp_data = await get_ltp(payload['symbol'])
        for k in ltp_data['data'].keys():
            ltp = ltp_data['data'][k]['last_price']
        payload['close_price'] = ltp
        payload['close_time'] = str(datetime.datetime.now())
        response = await close_order(order_id,**payload)
        transaction_detail = {
            "amount": ltp * payload['quantity'] * payload['lot_size'],
            "user_id": payload['user_id'],
            "for_id":response,
            "transaction_for":"close_order",
            "transaction_type":"CR",
            # "created_by" :request.state.user_id
        }
        await create_transaction(**transaction_detail)
        return {"data":{"message":"order closed succesfull", "order_id":response}}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get("/order/{order_id}")
async def get_single_order(request:Request,order_id:int):
    open_orders = await fetch_single_orders(order_id)
    return {"data":open_orders}


@router.get("/order/filter/user/{user_id}/type/{order_type}")
async def get_filter_order(request:Request,user_id:int, order_type:str):
    all_order = await fetch_all_filtered_orders(order_type,user_id)
    return {"data":all_order}


