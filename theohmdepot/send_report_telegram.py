
import requests

BOT_TOKEN = "7697633777:AAFmp0cVwJuXIGrtFstkz69Lb_9hXkxdunM"
CHAT_ID = "5406491889"

def send_photo(path, caption=""):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(path, "rb") as photo:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"photo": photo})

def send_document(path, caption=""):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(path, "rb") as doc:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"document": doc})

if __name__ == "__main__":
    send_photo("/mnt/data/top_nodi_real.png", "Top 3 nodi per ROI medio")
    send_photo("/mnt/data/backtest_real.png", "Simulazione ROI cumulato per giorno")
    send_document("/mnt/data/NodaIQ_Insights_Report_REAL.pdf", "📄 Report PDF - NodaIQ Insights")
