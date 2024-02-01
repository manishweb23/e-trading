from sqlalchemy import Column, Integer, String, Float, text, DateTime, func, Boolean
from db_config import Base, db, connection, engine


class Limit(Base):
    __tablename__ = "tbl_limit"
    id = Column(Integer, primary_key=True ,index=True)
    user_id = Column(Integer)
    amount = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer)


# Create the table in the database
Base.metadata.create_all(bind=engine)


async def create_limit(**payload):
    try:
        new_limit = Limit(
            user_id=payload['user_id'],
            amount=payload['amount'],
            created_by = payload['created_by']
            )
        db.add(new_limit)
        db.commit()
        limit_id = new_limit.id
        db.close()
        return limit_id
    except Exception as e:
        print(e)
        return False


async def update_limit(limit_id: int, **payload):
    try:
        # Query the existing order by its ID
        existing_limit = db.query(Limit).filter_by(id=limit_id).first()
        # Check if the order exists
        if existing_limit:
            # Update the fields with the new values from the payload
            existing_limit.close_price = payload.get('amount', existing_limit.amount)
            # existing_limit.quantity = payload.get('quantity', existing_limit.quantity)
            # existing_limit.lot_size = payload.get('lot_size', existing_limit.lot_size)
            # existing_limit.close_time = payload.get('close_time', existing_limit.close_time)

            # Commit the changes to the database
            db.commit()
            trade_id =existing_limit.id
            db.close()
            return trade_id
        else:
            return False
    except Exception as e:
        # Handle exceptions, log the error, or return False based on your requirements
        return False


async def fetch_limit(user_id):
    try:
        # Query orders with a specific symbol
        filtered_limit = db.query(Limit).filter(Limit.id == user_id).all()
        # You can now use the 'filtered_orders' list
        return filtered_limit[0]
    except Exception as e:
        # Handle exceptions, log the error, or return an empty list based on your requirements
        return e