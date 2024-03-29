from sqlalchemy import create_engine, Column, Integer, String, Float, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config


class Order(Base):
    __tablename__ = "tbl_order"
    id = Column(Integer, primary_key=True ,index=True)
    user_id = Column(Integer, index=True)
    symbol = Column(String, index=True)
    exchange = Column(String)
    trade_type = Column(String)
    expiry_date = Column(String, nullable=True)
    open_price = Column(Float, nullable=True)
    close_price = Column(Float, nullable=True)
    open_ticker = Column(Float, nullable=True)
    close_ticker = Column(Float, nullable=True)
    stop_loss = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=True)
    lot_size = Column(Integer, nullable=True)
    order_time_chart = Column(String, nullable=True)
    open_time = Column(String, nullable=True)
    close_time = Column(String, nullable=True)



async def open_order(**payload):
    try:
        new_trade = Order(
            user_id=payload['user_id'],
            symbol=payload['symbol'],
            exchange=payload['exchange'],
            trade_type=payload['trade_type'],
            expiry_date=payload['expiry_date'],
            open_price=payload['open_price'],
            stop_loss=payload['stop_loss'],
            quantity=payload['quantity'],
            lot_size=payload['lot_size'],
            order_time_chart=payload['order_time_chart'],
            open_time=payload['open_time'],
            )
        db.add(new_trade)
        db.commit()
        trade_id =new_trade.id
        db.close()
        return trade_id
    except Exception as e:
        return False
    

async def close_order(order_id: int, **payload):
    try:
        # Query the existing order by its ID
        existing_order = db.query(Order).filter_by(id=order_id).first()
        # Check if the order exists
        if existing_order:
            # Update the fields with the new values from the payload
            existing_order.close_price = payload.get('close_price', existing_order.close_price)
            # existing_order.quantity = payload.get('quantity', existing_order.quantity)
            # existing_order.lot_size = payload.get('lot_size', existing_order.lot_size)
            existing_order.close_time = payload.get('close_time', existing_order.close_time)

            # Commit the changes to the database
            db.commit()
            trade_id =existing_order.id
            db.close()
            return trade_id
        else:
            return False
    except Exception as e:
        # Handle exceptions, log the error, or return False based on your requirements
        return False


async def fetch_closed_orders():
    try:
        # Query orders with a specific symbol
        filtered_orders = db.query(Order).filter(Order.close_price != None).all()

        # You can now use the 'filtered_orders' list
        return filtered_orders
    except Exception as e:
        # Handle exceptions, log the error, or return an empty list based on your requirements
        return e
    

async def fetch_single_orders(order_id):
    try:
        # Query orders with a specific symbol
        filtered_orders = db.query(Order).filter(Order.id == order_id).all()

        # You can now use the 'filtered_orders' list
        return filtered_orders
    except Exception as e:
        # Handle exceptions, log the error, or return an empty list based on your requirements
        return e
    

async def fetch_all_filtered_orders(type,user_id):
    try:
        if type == 'open':
            # Query orders with a specific symbol
            filtered_orders = db.query(Order).filter(Order.user_id == user_id, Order.close_price == None).all()
        if type == 'close':
            # Query orders with a specific symbol
            filtered_orders = db.query(Order).filter(Order.user_id == user_id, Order.close_price != None).all()
        if type == 'all':
            # Query orders with a specific symbol
            filtered_orders = db.query(Order).filter(Order.user_id == user_id).all()

        # You can now use the 'filtered_orders' list
        return filtered_orders
    except Exception as e:
        # Handle exceptions, log the error, or return an empty list based on your requirements
        return e
    

async def fetch_instrument_all(instrument_type):
    # Execute a raw SQL query
    sql_query = text("SELECT * FROM view_instruments where instrument_type=:instrument_type ")
    print(sql_query)
    result = connection.execute(sql_query,{'instrument_type':instrument_type})
    # Fetch the results
    rows = result.fetchall()
    # print(rows)
    res = [list(row) for row in rows]
    # Close the result and engine
    return res


async def filter_instrument(symbol):
    # Execute a raw SQL query
    sql_query = text("SELECT * FROM tbl_instruments WHERE tradingsymbol LIKE :symbol")
    result = connection.execute(sql_query, {'symbol':symbol+'%'})

    # Fetch the results
    rows = result.fetchall()

    # Close the result and engine
    res = [list(row) for row in rows]
    # Close the result and engine
    return res



# # user model

# class User(Base):
#     __tablename__ = "tbl_user"
    
#     id = Column(Integer, primary_key=True ,index=True)
#     symbol = Column(String, index=True)
#     exchange = Column(String)
#     trade_type = Column(String)
#     expiry_date = Column(String, nullable=True)
#     open_price = Column(Float, nullable=True)
#     close_price = Column(Float, nullable=True)
#     open_ticker = Column(Float, nullable=True)
#     close_ticker = Column(Float, nullable=True)
#     stop_loss = Column(Float, nullable=True)
#     quantity = Column(Integer, nullable=True)
#     lot_size = Column(Integer, nullable=True)
#     order_time_chart = Column(String, nullable=True)
#     open_time = Column(String, nullable=True)
#     close_time = Column(String, nullable=True)



    