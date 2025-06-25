
import requests
import pandas as pd
from datetime import datetime
import os

BOT_TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'
LOG_PATH = 'logs/telegram_log.csv'

def log_message(content):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().isoformat()
    log_entry = pd.DataFrame([[timestamp, content]], columns=["timestamp", "message"])
    if os.path.exists(LOG_PATH):
        log_entry.to_csv(LOG_PATH, mode='a', header=False, index=False)
    else:
        log_entry.to_csv(LOG_PATH, index=False)

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    log_message(text)
