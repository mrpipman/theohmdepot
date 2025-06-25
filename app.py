
import streamlit as st
import dashboard
import help_page

st.set_page_config(layout="wide", page_title="Ω Depot", page_icon="🔮")

st.sidebar.title("Ω Menu")
selection = st.sidebar.radio("Vai a", ["📊 Dashboard", "❓ Help"])

if selection == "📊 Dashboard":
    dashboard.show()
elif selection == "❓ Help":
    help_page.show()
