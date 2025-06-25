
import streamlit as st
from pages import dashboard, help_page

st.set_page_config(layout="wide", page_title="Ω Depot", page_icon="🔮")

# Sidebar navigation
st.sidebar.title("Ω Menu")
selection = st.sidebar.radio("Vai a", ["🏠 Home", "📊 Dashboard", "❓ Help"])

# Layout wide + rimuovi footer
hide_st_style = '''
    <style>
    footer {visibility: hidden;}
    </style>
'''
st.markdown(hide_st_style, unsafe_allow_html=True)

# Page routing
if selection == "🏠 Home":
    st.markdown("# Benvenuto in Ω Depot")
    st.markdown("Questa è la piattaforma decisionale per analisi e backtest sui nodi.")
elif selection == "📊 Dashboard":
    dashboard.show()
elif selection == "❓ Help":
    help_page.show()
