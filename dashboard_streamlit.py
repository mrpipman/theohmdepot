import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os
from sklearn.cluster import KMeans

# --- CONFIGURAZIONE ---
DB_FILE = "arbitrage_trades.db"
st.set_page_config(page_title="The Ω Depot Dashboard", layout="wide")

# --- LOGO e HEADER ---
st.image("/mnt/data/Cattura.PNG", width=60)
st.title("The Ω Depot")
st.caption("Dashboard di arbitraggio intelligente su LMP")

# --- FUNZIONI ---
@st.cache_data(ttl=60)
def load_data():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame()
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql("SELECT * FROM trades ORDER BY datetime DESC", conn, parse_dates=["datetime"])
    return df

# --- SIDEBAR FILTRI ---
st.sidebar.header("🔍 Filtri")
roi_min = st.sidebar.slider("ROI minimo (%)", min_value=-100, max_value=100, value=0)
date_range = st.sidebar.date_input("Intervallo temporale", [])

# --- CARICA DATI ---
df = load_data()
if df.empty:
    st.warning("Nessun dato disponibile nel database.")
    st.stop()

# --- CREAZIONE NODO ---
df["node"] = df["buy_node"] + " ➝ " + df["sell_node"]

# --- FILTRI APPLICATI ---
df["datetime"] = pd.to_datetime(df["datetime"])
if date_range and len(date_range) == 2:
    df = df[(df["datetime"].dt.date >= date_range[0]) & (df["datetime"].dt.date <= date_range[1])]
df = df[df["roi"] >= roi_min]
all_nodi = df["node"].unique().tolist()
nodi = st.sidebar.multiselect("Nodi da includere", options=all_nodi, default=all_nodi)
df = df[df["node"].isin(nodi)]

# --- KPI CARDS ---
col1, col2 = st.columns(2)
profitto_totale = df["net_profit_usd"].sum()
roi_medio = df["roi"].mean()
emoji = "📈" if roi_medio > 5 else ("📉" if roi_medio < 0 else "😐")
col1.metric("💰 Profitto Totale (USD)", f"${profitto_totale:,.2f}")
col2.metric(f"{emoji} ROI Medio (%)", f"{roi_medio:.2f}%")

# --- METRICHE STATISTICHE ---
st.subheader("📊 Metriche Statistiche")
sharpe_ratio = roi_medio / df["roi"].std() if df["roi"].std() != 0 else 0
volatilita = df["net_profit_usd"].std()
df_sorted = df.sort_values("datetime")
df_sorted["cumulative_profit"] = df_sorted["net_profit_usd"].cumsum()
drawdown = df_sorted["cumulative_profit"] - df_sorted["cumulative_profit"].cummax()
drawdown_max = drawdown.min()

st.write(f"**Sharpe Ratio**: {sharpe_ratio:.2f}")
st.write(f"**Volatilità (σ)**: {volatilita:.2f} USD")
st.write(f"**Drawdown massimo**: {drawdown_max:.2f} USD")

# --- GRAFICO INTERATTIVO ---
st.subheader("📈 Profitto Cumulativo")
fig = px.line(df_sorted, x="datetime", y="cumulative_profit", title="Profitto Cumulativo nel Tempo",
              labels={"datetime": "Data", "cumulative_profit": "Profitto USD"})
fig.update_traces(mode="lines+markers")
st.plotly_chart(fig, use_container_width=True)

# --- DISTRIBUZIONE ROI ---
st.subheader("📊 Distribuzione ROI")
fig_hist = px.histogram(df, x="roi", nbins=30, title="Distribuzione ROI (%)",
                        labels={"roi": "ROI (%)"})
st.plotly_chart(fig_hist, use_container_width=True)

fig_box = px.box(df, y="roi", points="all", title="Boxplot ROI")
st.plotly_chart(fig_box, use_container_width=True)

# --- CLUSTER NODI ---
st.subheader("🧠 Clusterizzazione nodi")
spread_avg = df.groupby("node")["roi"].mean().reset_index()
if len(spread_avg) >= 3:
    kmeans = KMeans(n_clusters=3, n_init="auto")
    spread_avg["cluster"] = kmeans.fit_predict(spread_avg[["roi"]])
    fig_cluster = px.scatter(spread_avg, x="node", y="roi", color="cluster",
                             title="Cluster nodi per ROI medio", labels={"roi": "ROI medio", "node": "Nodo"})
    st.plotly_chart(fig_cluster, use_container_width=True)

# --- HEATMAP NODO VS EXCHANGE ---
st.subheader("🔥 Heatmap ROI medio nodo vs exchange")
if "exchange" in df.columns:
    pivot = df.pivot_table(values="roi", index="node", columns="exchange", aggfunc="mean")
    fig_heatmap = px.imshow(pivot, text_auto=True, color_continuous_scale="RdYlGn",
                            title="Heatmap ROI medio nodo vs exchange")
    st.plotly_chart(fig_heatmap, use_container_width=True)

# --- TOP NODI ---
st.subheader("🚀 Top nodi da monitorare oggi")
top_nodi = df.groupby("node")["roi"].mean().sort_values(ascending=False).head(3)
st.table(top_nodi.reset_index().rename(columns={"roi": "ROI medio"}))

# --- BACKTEST ENGINE ---
st.subheader("🧪 Simulazione Backtest")
df_backtest = df.copy()
df_backtest["date"] = df_backtest["datetime"].dt.date
backtest = df_backtest.groupby("date")["net_profit_usd"].sum().cumsum().reset_index()
fig_backtest = px.line(backtest, x="date", y="net_profit_usd", title="Simulazione ROI cumulato per giorno",
                       labels={"date": "Data", "net_profit_usd": "ROI cumulato"})
st.plotly_chart(fig_backtest, use_container_width=True)

# --- TABELLA DATI ---
def highlight_roi(val):
    if val > 5:
        return 'background-color: #d4edda; color: green'
    elif val < 0:
        return 'background-color: #f8d7da; color: red'
    else:
        return 'background-color: #fff3cd; color: orange'

styled_df = df.style.applymap(highlight_roi, subset=["roi"])
st.subheader("📄 Tabella Operazioni")
st.dataframe(styled_df, use_container_width=True, hide_index=True)

# --- ESPORTAZIONE DATI ---
st.subheader("📤 Esporta dati")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Scarica CSV", csv, "trades_export.csv", "text/csv")

# --- RICARICA ---
if st.button("🔁 Ricarica"):
    st.cache_data.clear()
    st.experimental_rerun()

# --- INFO AUTOMAZIONE ---
st.sidebar.markdown("---")
st.sidebar.markdown("🕒 **Esecuzione automatica** ogni giorno alle 06:00 UTC")
st.sidebar.markdown("💬 **Telegram Alert** attivo per ROI > soglia")
