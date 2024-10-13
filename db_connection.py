import os
from psycopg2 import pool

def initialize_connection_pool():
  db_url = os.getenv("DB_URI")
  if db_url is None:
    raise ValueError("DB_URI environment variable not set")

  connection_pool = pool.SimpleConnectionPool(
    1,  # Minimum number of connections in the pool
    1,  # Maximum number of connections in the pool
    db_url
  )

  if connection_pool:
    print("Connection pool created successfully")

  return connection_pool