import streamlit as st
def is_demo_mode(): return st.secrets.get("demo", False)
def mask_sensitive_data(df): return df