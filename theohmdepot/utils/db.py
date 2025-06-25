
import sqlite3

def get_connection():
    return sqlite3.connect("arbitrage_trades.db")

# In futuro: switch a psycopg2 o mysql.connector
