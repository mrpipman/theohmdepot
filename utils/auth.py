
import streamlit as st

def check_auth():
    token = st.secrets.get("access_token", None)
    user_input = st.text_input("Inserisci il token di accesso:", type="password")
    if token and user_input != token:
        st.warning("Token non valido.")
        st.stop()
