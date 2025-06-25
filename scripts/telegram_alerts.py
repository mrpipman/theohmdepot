
import requests
import pandas as pd
from datetime import datetime

BOT_TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def check_trades_and_notify():
    df = pd.read_csv("data/roi_data.csv")
    df_today = df[df['date'] == datetime.today().strftime('%Y-%m-%d')]
    if df_today.empty:
        return

    first_trade = df_today.iloc[0]
    send_message(f"📈 Primo trade del giorno:
{first_trade.to_dict()}")

    high_roi = df_today[df_today["roi"] > 0.05]
    for _, row in high_roi.iterrows():
        send_message(f"🚀 ROI alto (>5%): {row['roi']:.2%} - {row['node']}")
