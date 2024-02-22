import pandas as pd
from sqlalchemy import create_engine

# Define the database connection string
# Replace 'username', 'password', 'hostname', 'port', and 'database_name' with your database credentials
db_connection_str = "postgresql://doadmin:AVNS_Vup-iqX_aat5zbfWH_f@db-postgresql-blr1-96014-do-user-6620209-0.c.db.ondigitalocean.com:25060/defaultdb"

# Create the database engine
engine = create_engine(db_connection_str)

# Read data from the Excel file into a pandas DataFrame
excel_file = 'NSE.csv'  # Replace with the path to your Excel file
df = pd.read_csv(excel_file)

# Rename columns to match the database table columns if necessary
df.rename(columns={
    'Instrument Key': 'instrument_key',
    'Exchange Token': 'exchange_token',
    'Tradingsymbol': 'tradingsymbol',
    'Name': 'name',
    'Last Price': 'last_price',
    'Expiry': 'expiry',
    'Strike': 'strike',
    'Tick Size': 'tick_size',
    'Lot Size': 'lot_size',
    'Instrument Type': 'instrument_type',
    'Option Type': 'option_type',
    'Exchange': 'exchange'
}, inplace=True)

# Insert data into the PostgreSQL database table
df.to_sql('tbl_instruments', engine, if_exists='append', index=False)

print("Data inserted successfully into PostgreSQL database.")
