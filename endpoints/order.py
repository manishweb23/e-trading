from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Optional
from utils import get_ltp, get_market_quotes, find_ask_price, find_bid_price
from models.order_model import open_order, close_order, fetch_all_filtered_orders, fetch_single_orders, fetch_all_filtered_orders_count
from models.transaction_model import create_transaction, fetch_balance
import datetime
from typing import List



router = APIRouter(
    prefix="/api/v1",
    tags=["order"],
    responses={404: {"description": "Not found"}},
)

class filter_order(BaseModel):
    order_id: Optional[int] = None
    user_id: Optional[int] = None
    symbol: List[str]
    exchange: Optional[str] = None
    trade_type: Optional[str] = None
    expiry_date: Optional[str] = None
    open_order: Optional[bool] = None
    close_order: Optional[bool] = None


class order(BaseModel):
    user_id: int
    symbol: Optional[str] = None
    trading_symbol: Optional[str] = None
    exchange: Optional[str] = None
    trade_type: Optional[str] = None
    equity_short: Optional[bool] = False
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
        quote_data = await get_market_quotes(payload['symbol'])
        
        for k in quote_data['data'].keys():
            if payload['equity_short'] is False:
                sell_data = quote_data['data'][k]['depth']['sell']
                open_price = find_ask_price(sell_data)  
            else:
                buy_data = quote_data['data'][k]['depth']['buy']
                open_price = find_ask_price(buy_data) 

        payload['open_price'] = open_price
        # validate with balance
        balance = await fetch_balance(request.state.user_id)
        if balance-payload['quantity']*payload['lot_size']*open_price < 0:
            return {"data":{"message":"Insuficeint balance!", "balance":balance}}
        payload['open_time'] = str(datetime.datetime.now())
        response = await open_order(**payload)
        transaction_detail = {
            "amount": open_price * payload['quantity'] * payload['lot_size'],
            "user_id": request.state.user_id,
            "for_id":response,
            "transaction_for":"open_order",
            "transaction_type":"DR",
            # "created_by" :request.state.user_id
        }
        await create_transaction(**transaction_detail)
        return {"data":{"message":"order succesfull", "order_id":response}}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail=e)


@router.put("/order/{order_id}")
async def update_order(request:Request,payload:order,order_id:int):
    payload = payload.dict()
    open_order = await fetch_single_orders(order_id)
    for i in open_order:
        if i.close_price:
            return {"data":{"message":"order already closed", "order_id":i.id}}
        open_order_quantity = i.quantity
        open_order_lot_size = i.lot_size
    try:
        quote_data = await get_market_quotes(payload['symbol'])
        for k in quote_data['data'].keys():
            if payload['equity_short'] is False:
                buy_data = quote_data['data'][k]['depth']['buy']
                close_price = find_ask_price(buy_data)  
            else:
                sell_data = quote_data['data'][k]['depth']['sell']
                close_price = find_ask_price(sell_data) 

        payload['close_price'] = close_price
        payload['close_time'] = str(datetime.datetime.now())
        response = await close_order(order_id,**payload)
        transaction_detail = {
            "amount": close_price * open_order_quantity * open_order_lot_size,
            "user_id": request.state.user_id,
            "for_id":response,
            "transaction_for":"close_order",
            "transaction_type":"CR",
            "created_by" :request.state.user_id
        }
        await create_transaction(**transaction_detail)
        return {"data":{"message":"order closed succesfull", "order_id":response}}
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)


@router.get("/order/{order_id}")
async def get_single_order(request:Request,order_id:int):
    open_orders = await fetch_single_orders(order_id)
    return {"data":open_orders}


@router.get("/order/filter/user/{user_id}/type/{order_type}")
async def get_filter_order(request:Request,user_id:int, order_type:str):
    all_order = await fetch_all_filtered_orders(order_type,user_id)
    return {"data":all_order}


@router.get("/order/filter/user/{user_id}/type/{order_type}/count")
async def get_filter_order_count(request:Request,user_id:int, order_type:str):
    all_order = await fetch_all_filtered_orders_count(order_type,user_id)
    return {"data":{'count':all_order}}


