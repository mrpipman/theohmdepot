
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from utils.helpers import highlight_roi
from utils.demo_mode import mask_sensitive_data
from utils.auth import check_auth
from sklearn.cluster import KMeans

def load_db_table(table_name):
    try:
        conn = sqlite3.connect("arbitrage_trades.db")
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception as e:
        st.warning(f"⚠️ Impossibile caricare tabella '{table_name}': {e}")
        return pd.DataFrame()

def show():
    check_auth()
    st.title("📊 Dashboard Operativa")

    df = load_db_table("entsoe_prices")
    if not df.empty:
        st.subheader("⚡ Prezzi ENTSO-E (Day Ahead)")
        st.dataframe(df)

    df = load_db_table("nordpool_prices")
    if not df.empty:
        st.subheader("❄️ Prezzi Nord Pool (Esempio Storico)")
        st.dataframe(df)

    # KPI demo - da mascherare in modalità demo
    df = load_db_table("entsoe_prices")
    if df.empty:
        return

    df = mask_sensitive_data(df)
    col1, col2 = st.columns(2)
    col1.metric("Prezzo medio", f"{df['price'].mean():.2f} €/MWh")
    col2.metric("Varianza", f"{df['price'].var():.2f}")

    st.line_chart(df.groupby("hour")["price"].mean(), use_container_width=True)
