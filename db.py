import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get('DB_HOST') 
DB_USER = os.environ.get('DB_USER') 
DB_PASS = os.environ.get('DB_PASS') 
DB_NAME = os.environ.get('DB_NAME') 

def connect():
    db = mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASS,
        database=DB_NAME
    )
    return db