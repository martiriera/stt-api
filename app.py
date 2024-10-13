import atexit
from psycopg2 import pool
from dotenv import load_dotenv
from flask import Flask

from db_connection import initialize_connection_pool
from queries import CREATE_TRANSCRIPTION_TABLE, INSERT_TRANSCRIPTION

load_dotenv()

app = Flask(__name__)

connection_pool = initialize_connection_pool()

@app.post("/transcribe")
def transcribe():
    text = "Hello, world!"
    conn = connection_pool.getconn()
    try:
        cur = conn.cursor()
        cur.execute(CREATE_TRANSCRIPTION_TABLE)
        cur.execute(INSERT_TRANSCRIPTION, (text,))
        transcription_id = cur.fetchone()[0]
        conn.commit()
        return {"id": transcription_id}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        connection_pool.putconn(conn)

# Register a function to close all connections in the pool when the server shuts down
@atexit.register
def close_connection_pool():
    if connection_pool:
        connection_pool.closeall()
        print("Connection pool closed successfully")