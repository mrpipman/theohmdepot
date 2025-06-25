
import streamlit as st

def is_demo_mode():
    return st.secrets.get("demo", False)

def mask_sensitive_data(df):
    if not is_demo_mode():
        return df
    df = df.copy()
    df['node'] = df['node'].apply(lambda x: "NODE_XXX")
    df['profit'] = 0
    return df
