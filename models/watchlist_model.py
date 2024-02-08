from sqlalchemy import Column, Integer, String, Float, text, DateTime, func
from db_config import Base, db, connection, engine


class Watchlist(Base):
    __tablename__ = "tbl_watchlist"
    id = Column(Integer, primary_key=True ,index=True)
    user_id = Column(Integer, index=True)
    symbol_name = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Create the table in the database
Base.metadata.create_all(bind=engine)


async def add_watchlist(**payload):
    try:
        new_watchlist = Watchlist(
            user_id=payload['user_id'],
            symbol_name=payload['symbol_name'],
            )
        db.add(new_watchlist)
        db.commit()
        new_watchlist_id =new_watchlist.id
        db.close()
        return new_watchlist_id
    except Exception as e:
        print(e)
        return False


async def fetch_watchlist(user_id):
    try:
        # Query orders with a specific symbol
        filtered_orders = db.query(Watchlist).filter(Watchlist.user_id == user_id).all()

        # You can now use the 'filtered_orders' list
        return filtered_orders
    except Exception as e:
        # Handle exceptions, log the error, or return an empty list based on your requirements
        return e
    
