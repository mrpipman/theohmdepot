
import streamlit as st
import sqlite3
import pandas as pd

def show():
    st.title("📊 Dashboard Operativa")

    try:
        conn = sqlite3.connect("arbitrage_trades.db")
        df = pd.read_sql("SELECT * FROM entsoe_prices", conn)
        conn.close()
        st.dataframe(df)
        st.line_chart(df.groupby("hour")["price"].mean())
    except Exception as e:
        st.error(f"Errore caricando i dati: {e}")
