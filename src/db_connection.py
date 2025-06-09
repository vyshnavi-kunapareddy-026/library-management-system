import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# Replace these with your actual PostgreSQL connection details

def get_connection(db_host, db_port, db_name, db_user, db_password):
    """
    Establishes and returns a connection to the PostgreSQL database.
    """
    try:
        # print(f"Connecting to the database...{db_port} {type(db_port)}")
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
            cursor_factory=RealDictCursor  # Makes cursor fetch dicts directly
        )
        print("Connection successful.")
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        return None
