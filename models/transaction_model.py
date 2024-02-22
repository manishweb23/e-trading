from sqlalchemy import Column, Integer, String, Float, text, DateTime, func
from db_config import Base, db, connection, engine


class Transaction(Base):
    __tablename__ = "tbl_transaction"
    id = Column(Integer, primary_key=True ,index=True)
    user_id = Column(Integer, index=True)
    amount = Column(Float)
    for_id = Column(Integer, index=True)
    transaction_for = Column(String)
    transaction_type = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, index=True)


# Create the table in the database
Base.metadata.create_all(bind=engine)

async def create_transaction(**payload):
    try:
        new_transaction = Transaction(
            user_id=payload['user_id'],
            amount=payload['amount'],
            for_id=payload['for_id'],
            transaction_for=payload['transaction_for'],
            transaction_type=payload['transaction_type'],
            )
        db.add(new_transaction)
        db.commit()
        transaction_id = new_transaction.id
        db.close()
        return transaction_id
    except Exception as e:
        print(e)
        return False


async def fetch_transaction(user_id):
    try:
        # Query orders with a specific symbol
        filtered_orders = db.query(Transaction).filter(Transaction.user_id == user_id).all()

        # You can now use the 'filtered_orders' list
        return filtered_orders
    except Exception as e:
        # Handle exceptions, log the error, or return an empty list based on your requirements
        return e
    


async def fetch_balance(user_id):
    try:
        sql_query = text("SELECT SUM(CASE WHEN transaction_type = 'CR' THEN amount WHEN transaction_type = 'DR' THEN -amount ELSE 0 END) AS available_balance FROM tbl_transaction WHERE user_id = :user_id")
        result = connection.execute(sql_query, {'user_id':user_id})

        # Fetch the results
        available_balance = result.fetchone()
        return available_balance[0]
    except Exception as e:
        # Handle exceptions, log the error, or return an empty list based on your requirements
        return e
    

async def fetch_pl(user_id):
    try:
        sql_query = text("SELECT SUM(CASE WHEN transaction_type = 'CR' THEN amount WHEN transaction_type = 'DR' THEN -amount ELSE 0 END) AS available_balance FROM tbl_transaction WHERE user_id = :user_id")
        result = connection.execute(sql_query, {'user_id':user_id})

        # Fetch the results
        available_balance = result.fetchone()
        return available_balance[0]
    except Exception as e:
        # Handle exceptions, log the error, or return an empty list based on your requirements
        return e