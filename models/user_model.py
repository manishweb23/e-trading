from sqlalchemy import Column, Integer, String, Float, text, DateTime, func, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from db_config import Base, db, connection, engine
from utils import md5_hash


class User(Base):
    __tablename__ = "tbl_user"
    id = Column(Integer, primary_key=True ,index=True)
    mobile = Column(String)
    password = Column(String)
    role = Column(ARRAY(String),default=["user"])
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Create the table in the database
Base.metadata.create_all(bind=engine)


async def create_user(**payload):
    try:
        new_user = User(
            mobile=payload['mobile'],
            password=md5_hash(payload['password'])
            )
        db.add(new_user)
        db.commit()
        user_id = new_user.id
        db.close()
        return user_id
    except Exception as e:
        print(e)
        return False


async def fetch_user(user_id):
    try:
        # Query orders with a specific symbol
        filtered_orders = db.query(User).filter(User.id == user_id).all()
        # You can now use the 'filtered_orders' list
        return filtered_orders[0]
    except Exception as e:
        # Handle exceptions, log the error, or return an empty list based on your requirements
        return e