from sqlalchemy import Column, Integer, String, Float, text,desc,Boolean,func
from db_config import Base, db, connection, engine


class Order(Base):
    __tablename__ = "tbl_order"
    id = Column(Integer, primary_key=True ,index=True)
    user_id = Column(Integer, index=True)
    symbol = Column(String, index=True)
    trading_symbol = Column(String, index=True)
    exchange = Column(String)
    trade_type = Column(String)
    order_short = Column(Boolean, default=False, nullable=True)
    intraday = Column(Boolean, default=False, nullable=True)
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


# Create the table in the database
Base.metadata.create_all(bind=engine)


async def open_order(**payload):
    try:
        new_trade = Order(
            user_id=payload['user_id'],
            symbol=payload['symbol'],
            trading_symbol=payload['trading_symbol'],
            exchange=payload['exchange'],
            trade_type=payload['trade_type'],
            order_short=payload['order_short'],
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
        print(e)
        return False
    

async def close_order(order_id: int, **payload):
    try:
        # Query the existing order by its ID
        existing_order = db.query(Order).filter_by(id=order_id).first()
        # Check if the order exists
        if existing_order:
            # Update the fields with the new values from the payload
            existing_order.close_price = payload.get('close_price', existing_order.close_price)
            existing_order.close_time = payload.get('close_time', existing_order.close_time)

            # Commit the changes to the database
            db.commit()
            trade_id =existing_order.id
            db.close()
            print(trade_id)
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
            filtered_orders = db.query(Order).filter(Order.user_id == user_id, Order.close_price == None).order_by(desc(Order.id)).all()
        if type == 'close':
            # Query orders with a specific symbol
            filtered_orders = db.query(Order).filter(Order.user_id == user_id, Order.close_price != None).order_by(desc(Order.id)).all()
        if type == 'all':
            print("all order")
            # Query orders with a specific symbol
            filtered_orders = db.query(Order).filter(Order.user_id == user_id).all()

        # You can now use the 'filtered_orders' list
        return filtered_orders
    except Exception as e:
        # Handle exceptions, log the error, or return an empty list based on your requirements
        print(e)
        return {'data':{'message':'something went wrong!'}}
    

async def fetch_trading_balance(user_id):
    try:
        sql_query = text("SELECT * FROM tbl_order WHERE user_id = :user_id and close_price is null")
        result = connection.execute(sql_query, {'user_id':user_id})

        # Fetch the results
        available_balance = 0
        balance_data = result.fetchall()
        for balance in balance_data:
            available_balance = available_balance + balance[8]*balance[13]*balance[14]
        return available_balance
    except Exception as e:
        # Handle exceptions, log the error, or return an empty list based on your requirements
        return e
    

async def fetch_all_filtered_orders_count(type,user_id):
    try:
        if type == 'open':
            # Query orders with a specific symbol
            filtered_orders = db.query(func.count(func.distinct(Order.id))).filter(Order.user_id == user_id, Order.close_price == None).scalar()
        if type == 'close':
            filtered_orders = db.query(func.count(func.distinct(Order.id))).filter(Order.user_id == user_id, Order.close_price != None).scalar()
        if type == 'all':
            filtered_orders = db.query(func.count(func.distinct(Order.id))).filter(Order.user_id == user_id).scalar()

        # You can now use the 'filtered_orders' list
        return filtered_orders
    except Exception as e:
        # Handle exceptions, log the error, or return an empty list based on your requirements
        return e

async def fetch_instrument_all(instrument_type,name,limit,offset):
    # Execute a raw SQL query
    sql_query = text("SELECT * FROM tbl_instruments where instrument_type like :instrument_type and option_type in ('CE','PE') and is_active = TRUE limit :limit offset :offset")
    if instrument_type in ['OPTIDX','OPTSTK','OPTCUR','OPTCOM','FUTIDX','FUTSTK','FUTCUR','FUTCOM']:
        sql_query = text("SELECT * FROM tbl_instruments where instrument_type like :instrument_type  and option_type in ('CE','PE') AND TO_DATE(expiry,'YYYY-MM-DD') >= CURRENT_DATE and is_active = TRUE limit :limit offset :offset")
    filter_data = {'instrument_type': instrument_type, 'limit':limit, 'offset':offset}
    if name != None:
        sql_query = text("SELECT * FROM tbl_instruments where instrument_type like :instrument_type and (name like :name or tradingsymbol like :tradingsymbol) and option_type in ('CE','PE') and is_active = TRUE limit :limit offset :offset")

        if instrument_type in ['OPTIDX','OPTSTK','OPTCUR','OPTCOM','FUTIDX','FUTSTK','FUTCUR','FUTCOM']:
            sql_query = text("SELECT * FROM tbl_instruments where instrument_type like :instrument_type and (name like :name or tradingsymbol like :tradingsymbol) and option_type in ('CE','PE') AND TO_DATE(expiry,'YYYY-MM-DD') >= CURRENT_DATE and is_active = TRUE limit :limit offset :offset")

        filter_data = {'instrument_type': instrument_type,'name':'%'+name+'%', 'tradingsymbol':name+'%','limit':limit, 'offset':offset}
    result = connection.execute(sql_query,filter_data)
    # Fetch the results
    rows = result.fetchall()
    # print(rows)
    res = [list(row) for row in rows]
    # Close the result and engine
    return res


async def filter_instrument(symbol,expiry):
    # Execute a raw SQL query
    sql_query = text("SELECT * FROM tbl_instruments WHERE tradingsymbol LIKE :symbol and expiry = :expiry and is_active = TRUE")
    result = connection.execute(sql_query, {'symbol':'%'+symbol+'%', 'expiry':expiry})

    # Fetch the results
    rows = result.fetchall()

    # Close the result and engine
    res = [list(row) for row in rows]
    # Close the result and engine
    return res


async def filter_instrument_expiry(symbol):
    # Execute a raw SQL query
    sql_query = text("""
            select
                expiry
            from
                tbl_instruments
            where
                tradingsymbol like :symbol
                and TO_DATE(expiry,
                'YYYY-MM-DD') >= CURRENT_DATE
                and is_active = TRUE
            group by
                expiry
            order by
                expiry;
    """)
    result = connection.execute(sql_query, {'symbol':symbol+'%'})

    # Fetch the results
    rows = result.fetchall()

    # Close the result and engine
    res = [list(row)[0] for row in rows]
    # Close the result and engine
    return res



async def filter_instrument_name(name, limit, offset):
    # Execute a raw SQL query
    sql_query = text("""
            select
                *
            from
                tbl_instruments
            where
                name like :name 
                and name is not null
                and is_active = TRUE
            order by
                name
            limit :limit offset :offset;
    """)
    result = connection.execute(sql_query, {'name':'%'+name+'%', 'limit':limit, 'offset':offset})

    # Fetch the results
    rows = result.fetchall()

    # Close the result and engine
    res = [list(row) for row in rows]
    # Close the result and engine
    return res

async def filter_instrument_all(limit:int=10,offset:int=0):
    # Execute a raw SQL query
    sql_query = text("""
            select
                *
            from
                tbl_instruments
            where is_active = TRUE
            order by name
                limit :limit offset :offset;
        """)
    result = connection.execute(sql_query, {'limit':limit,'offset':offset})

    # Fetch the results
    rows = result.fetchall()

    # Close the result and engine
    res = [list(row) for row in rows]
    # Close the result and engine
    return res

