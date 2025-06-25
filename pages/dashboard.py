
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import load_data, highlight_roi
from utils.demo_mode import mask_sensitive_data
from utils.auth import check_auth
from sklearn.cluster import KMeans

def show():
    check_auth()
    st.title("📊 Dashboard Operativa")

    df = load_data()
    df = mask_sensitive_data(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("ROI Medio", f"{df['roi'].mean():.2%}")
    col2.metric("Profitto Totale", f"${df['profit'].sum():,.2f}")
    col3.metric("Drawdown Max", f"{df['drawdown'].min():.2%}")
    col4.metric("Sharpe Ratio", f"{(df['roi'].mean()/df['roi'].std()):.2f}")

    st.subheader("📈 ROI - Andamento nel tempo")
    st.plotly_chart(px.line(df, x="date", y="roi"), use_container_width=True)

    st.subheader("📉 Distribuzione ROI")
    st.plotly_chart(px.histogram(df, x="roi", nbins=30), use_container_width=True)

    st.subheader("📦 Boxplot ROI per nodo")
    st.plotly_chart(px.box(df, x="node", y="roi"), use_container_width=True)

    st.subheader("🔥 Heatmap Nodi vs Exchange")
    pivot = df.pivot_table(index="node", columns="exchange", values="roi", aggfunc="mean").fillna(0)
    fig_heatmap = go.Figure(data=go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index, colorscale='Viridis'))
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.subheader("🧠 Cluster Nodi Ricorrenti")
    node_group = df.groupby("node")[["roi", "profit"]].mean()
    kmeans = KMeans(n_clusters=3, n_init=10).fit(node_group)
    node_group["cluster"] = kmeans.labels_
    fig_cluster = px.scatter(node_group, x="roi", y="profit", color="cluster", hover_name=node_group.index)
    st.plotly_chart(fig_cluster, use_container_width=True)

    st.subheader("🧪 Simulazione Backtest")
    selected_node = st.selectbox("Seleziona nodo", df["node"].unique())
    st.line_chart(df[df["node"] == selected_node][["date", "roi"]].set_index("date"))

    st.subheader("📋 Tabella Trade")
    st.dataframe(df.style.apply(highlight_roi, axis=1), use_container_width=True)

    st.download_button("⬇️ Scarica CSV", data=df.to_csv(index=False), file_name="report.csv", mime="text/csv")
    st.download_button("⬇️ Scarica Excel", data=df.to_excel(index=False), file_name="report.xlsx", mime="application/vnd.ms-excel")

    if st.button("🔄 Aggiorna dati"):
        st.experimental_rerun()
