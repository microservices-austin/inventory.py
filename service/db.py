"""
Handle Database Layer
"""
import psycopg2
from service.constants import DB_HOST, DB_USER, DB_PASS

def connect_db():
    """
    Connect to database
    :return: Database cursor
    """
    conn = psycopg2.connect(dbname='inventory', user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor()
    return cur
