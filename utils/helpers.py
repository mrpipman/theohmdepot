
import pandas as pd

def load_data():
    return pd.read_csv("data/roi_data.csv")

def highlight_roi(row):
    color = "background-color: lightgreen" if row['roi'] > 0 else "background-color: pink"
    return [color if col == 'roi' else "" for col in row.index]
