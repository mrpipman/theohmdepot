
import schedule
import time
import shutil
from datetime import datetime
from send_report_telegram import send_document

def backup_db():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy('arbitrage_trades.db', f'backups/arbitrage_trades_{timestamp}.db')
    print(f"Backup completato: {timestamp}")

def send_morning_report():
    send_document('report.pdf', caption="📈 Report giornaliero Ω Depot")

schedule.every().day.at("08:00").do(send_morning_report)
schedule.every().day.at("02:00").do(backup_db)

while True:
    schedule.run_pending()
    time.sleep(60)
