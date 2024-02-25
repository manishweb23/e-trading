from sqlalchemy import create_engine

# Define the database connection string
# Replace 'username', 'password', 'hostname', 'port', and 'database_name' with your database credentials
db_connection_str = "postgresql://doadmin:AVNS_Vup-iqX_aat5zbfWH_f@db-postgresql-blr1-96014-do-user-6620209-0.c.db.ondigitalocean.com:25060/defaultdb"

# Create the database engine
engine = create_engine(db_connection_str)

# Execute an ALTER TABLE query to rename the table
rename_query = """ALTER TABLE tbl_instruments RENAME TO tbl_instruments_old;"""

try:
    # Execute the query
    with engine.connect() as connection:
        connection.execute(rename_query)
    print("Table renamed successfully.")
except Exception as e:
    print("Error:", e)
# 