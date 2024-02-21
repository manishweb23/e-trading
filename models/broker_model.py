from sqlalchemy import Column, Integer, String, Float, text, DateTime, func, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from db_config import Base, db, connection, engine
from typing import desc
from utils import md5_hash


class Broker(Base):
    __tablename__ = "tbl_broker"
    id = Column(Integer, primary_key=True ,index=True)
    code = Column(String)
    token = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Create the table in the database
Base.metadata.create_all(bind=engine)


async def create_token(**payload):
    try:
        new_token = Broker(
            code=payload['code'],
            token=md5_hash(payload['token'])
            )
        db.add(new_token)
        db.commit()
        token_id = new_token.id
        db.close()
        return token_id
    except Exception as e:
        print(e)
        return False


async def fetch_token():
    try:
        # Query orders with a specific symbol
        filtered_broker = db.query(Broker).order_by(desc(Broker.id)).first()
        # You can now use the 'filtered_orders' list
        return filtered_broker[0]
    except Exception as e:
        # Handle exceptions, log the error, or return an empty list based on your requirements
        return e