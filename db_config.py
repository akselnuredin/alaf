import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

# Connection pool
connection_pool = None

def initialize_pool():
    """Initialize the connection pool"""
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 10,  # min and max connections
            **DB_CONFIG
        )
        print("Connection pool created successfully")
    except Exception as e:
        print(f"Error creating connection pool: {e}")

def get_connection():
    """Get a connection from the pool"""
    if connection_pool:
        return connection_pool.getconn()
    return None

def return_connection(connection):
    """Return a connection to the pool"""
    if connection_pool:
        connection_pool.putconn(connection)

def close_all_connections():
    """Close all connections in the pool"""
    if connection_pool:
        connection_pool.closeall()
