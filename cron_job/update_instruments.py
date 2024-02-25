"""
Run every day at 6AM +5.30GMT for update latest instruments details into db.

"""


import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import os
from datetime import datetime
import requests
import gzip
import shutil

# Define the database connection string
# Replace 'username', 'password', 'hostname', 'port', and 'database_name' with your database credentials
db_connection_str = "postgresql://doadmin:AVNS_Vup-iqX_aat5zbfWH_f@db-postgresql-blr1-96014-do-user-6620209-0.c.db.ondigitalocean.com:25060/defaultdb"

# Define the URL to download the CSV file
url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
csv_filename = "complete.csv.gz"

# Download the CSV file
response = requests.get(url)
with open(csv_filename, "wb") as f:
    f.write(response.content)

# Extract the data from the downloaded CSV file
with gzip.open(csv_filename, 'rb') as f_in:
    with open('complete.csv', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

# Check if old CSV file exists and delete it
if os.path.exists(csv_filename):
    os.remove(csv_filename)

# Create the database engine
engine = create_engine(db_connection_str)

with engine.connect() as conn:
    conn.execute(text("UPDATE tbl_instruments SET is_active = FALSE"))

# Read data from the CSV file into a pandas DataFrame
df = pd.read_csv("complete.csv")

# Add necessary columns
df['created_date'] = datetime.now()
df['is_active'] = True

# Insert data into the PostgreSQL database table
df.to_sql('tbl_instruments', engine, if_exists='append', index=False)

print("Data inserted successfully into PostgreSQL database.")
