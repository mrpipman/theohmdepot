
import pandas as pd
import sqlite3
from utils.feed_parser import (
    fetch_entsoe_day_ahead_price,
    fetch_nordpool_example_csv
)

def save_to_db(df: pd.DataFrame, table_name: str, db_path='arbitrage_trades.db'):
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"✅ Dati salvati in tabella '{table_name}' nel DB {db_path}")

def ingest_entsoe(api_key: str):
    df = fetch_entsoe_day_ahead_price(api_key=api_key)
    save_to_db(df, "entsoe_prices")

def ingest_nordpool():
    df = fetch_nordpool_example_csv()
    save_to_db(df, "nordpool_prices")

if __name__ == "__main__":
    # ESEMPIO USO: Ingerimento manuale
    ingest_nordpool()
    # ingest_entsoe(api_key="YOUR_TOKEN")
