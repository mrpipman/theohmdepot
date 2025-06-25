
import streamlit as st
import pandas as pd
import sqlite3
import time

DB_FILE = "arbitrage_trades.db"

st.set_page_config(page_title="Arbitrage Bot Dashboard", layout="wide")
st.title("📈 Energy Arbitrage Trading Dashboard")

# Carica dati dal database
@st.cache_data(ttl=60)
def load_data():
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql("SELECT * FROM trades ORDER BY datetime DESC", conn, parse_dates=["datetime"])
    return df

# Aggiornamento in tempo reale
data_placeholder = st.empty()

while True:
    df = load_data()
    if df.empty:
        st.warning("Nessuna operazione disponibile nel database.")
    else:
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime", ascending=False)

        data_placeholder.dataframe(df, use_container_width=True, height=600)

        profit = df["net_profit_usd"].sum()
        roi_avg = df["roi"].mean()

        st.metric("📊 Profitto Totale ($)", f"{profit:,.2f}")
        st.metric("📈 ROI Medio (%)", f"{roi_avg * 100:.2f}%")

    time.sleep(60)
    st.rerun()
