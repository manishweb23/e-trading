from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config 

engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Create the SQLite database in memory (replace with your actual database URL)
DATABASE_URL = config.DATABASE_URL
# engine = create_engine(DATABASE_URL)
connection = engine.connect()

# Create a session to interact with the database
# SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)
db = SessionLocal()


# Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()