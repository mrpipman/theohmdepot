import pandas as pd
import matplotlib.pyplot as plt
import time
import os
import requests
from io import StringIO
from datetime import datetime, timedelta

# CONFIGURAZIONE BOT
BUDGET_EUR = 500                # Budget in euro per test
USD_PER_EUR = 1.08              # Tasso di cambio EUR -> USD
BUDGET_USD = BUDGET_EUR * USD_PER_EUR
SPREAD_THRESHOLD = 5            # minimo spread per agire ($/MWh)
MAX_MWH_PER_HOUR = 100          # limite operativo realistico
TRADING_FEE = 0.002             # 0.2% fee
SLIPPAGE = 0.01                 # 1% slippage sulle operazioni
OUTPUT_FILE = "arbitrage_output.csv"

# TELEGRAM CONFIG
TELEGRAM_TOKEN = "7697633777:AAFmp0cVwJuXIGrtFstkz69Lb_9hXkxdunM"
TELEGRAM_CHAT_ID = "5406491889"

# WHITELIST nodi affidabili (esempio base)
TRUSTED_NODES = set(["PJM-RTO", "MID-ATL/APS", "ALDENE", "ATHENIA", "CONED", "BOSTON", "NEW YORK", "SPRINGFIELD"])

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception as e:
        print("[TELEGRAM ERRORE]", e)
        return False

# Calcola la data del giorno precedente in formato richiesto
def get_latest_date_string():
    yesterday = datetime.utcnow() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%dT00:00Z"), yesterday.strftime("%Y%m%d")

# DOWNLOAD DATI PUBBLICI

def download_pjm():
    date_str, _ = get_latest_date_string()
    url = f"https://dataminer2.pjm.com/feed/rt_hrl_lmps/{date_str}"
    r = requests.get(url)
    return pd.read_csv(StringIO(r.text))

def download_nyiso():
    _, date_str = get_latest_date_string()
    url = f"https://www.nyiso.com/documents/20142/29244401/rtlbmp_{date_str}.csv"
    r = requests.get(url)
    return pd.read_csv(StringIO(r.text))

def download_isone():
    yesterday = datetime.utcnow() - timedelta(days=1)
    date_str = yesterday.strftime("%Y%m%d")
    url = f"https://www.iso-ne.com/static-assets/documents/2024/01/{date_str}_da_lmp.csv"
    r = requests.get(url)
    return pd.read_csv(StringIO(r.text))

# CARICAMENTO DATI MULTI-MERCATO

def load_and_merge_data():
    dfs = []
    try:
        pjm = download_pjm()
        pjm = pjm[pjm["type"] == "LOAD"]
        pjm = pjm[["datetime_beginning_utc", "pnode_name", "total_lmp_rt"]]
        pjm.columns = ["datetime", "node", "lmp"]
        pjm["datetime"] = pd.to_datetime(pjm["datetime"])
        dfs.append(pjm)
    except Exception as e:
        print("[PJM ERROR]", e)

    try:
        nyiso = download_nyiso()
        nyiso = nyiso[["Time Stamp", "Name", "LBMP"]]
        nyiso.columns = ["datetime", "node", "lmp"]
        nyiso["datetime"] = pd.to_datetime(nyiso["datetime"])
        dfs.append(nyiso)
    except Exception as e:
        print("[NYISO ERROR]", e)

    try:
        isone = download_isone()
        isone = isone[["Hour Ending", "Location Name", "Locational Marginal Price ($/MWh)"]]
        isone.columns = ["datetime", "node", "lmp"]
        isone["datetime"] = pd.to_datetime(isone["datetime"], errors='coerce')
        dfs.append(isone)
    except Exception as e:
        print("[ISONE ERROR]", e)

    return pd.concat(dfs, ignore_index=True)

# STRATEGIA ARBITRAGGIO MIGLIORATA

def run_arbitrage(df):
    results = []
    global BUDGET_USD
    for ts, group in df.groupby("datetime"):
        group = group[group["node"].isin(TRUSTED_NODES)]
        if len(group) < 2:
            continue

        group = group.sort_values("lmp")
        min_row = group.iloc[0]
        max_row = group.iloc[-1]

        spread = max_row.lmp - min_row.lmp
        dynamic_threshold = group["lmp"].std() * 1.5
        if spread < max(SPREAD_THRESHOLD, dynamic_threshold) or min_row.lmp <= 0:
            continue

        capital_limit = BUDGET_USD * 0.25
        buy_price = min_row.lmp * (1 + SLIPPAGE)
        mwh = min(capital_limit / buy_price, MAX_MWH_PER_HOUR)
        sell_price = max_row.lmp * (1 - SLIPPAGE)

        gross_profit = mwh * (sell_price - buy_price)
        fee = mwh * (sell_price + buy_price) * TRADING_FEE
        net_profit = gross_profit - fee

        if net_profit <= 0:
            continue

        BUDGET_USD += net_profit  # reinvestimento

        roi = net_profit / (mwh * buy_price)
        results.append({
            "datetime": ts,
            "buy_node": min_row.node,
            "sell_node": max_row.node,
            "buy_price": buy_price,
            "sell_price": sell_price,
            "spread": spread,
            "mwh_traded": mwh,
            "gross_profit_usd": gross_profit,
            "fee_usd": fee,
            "net_profit_usd": net_profit,
            "roi": roi
        })
    return pd.DataFrame(results)

# VISUALIZZAZIONE GRAFICO PROFITTI

def plot_profits(df):
    df_sorted = df.sort_values("datetime")
    df_sorted["cumulative_profit"] = df_sorted["net_profit_usd"].cumsum()
    plt.figure(figsize=(12, 6))
    plt.plot(df_sorted["datetime"], df_sorted["cumulative_profit"], label="Profitto Cumulativo ($)", color='green')
    plt.xlabel("Data/Ora")
    plt.ylabel("Profitto ($)")
    plt.title("Performance cumulativa del bot di arbitraggio")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("profit_chart.png")
    plt.show()

# AVVIO DIRETTO
if __name__ == "__main__":
    print("[BOT] Avvio test multi-mercato...")
    df_all = load_and_merge_data()
    if df_all.empty:
        print("[BOT] Nessun dato disponibile.")
    else:
        results = run_arbitrage(df_all)
        total = results["net_profit_usd"].sum()
        print(f"[BOT] Profitto stimato: ${total:,.2f} su {len(results)} operazioni.")
        send_telegram_message(f"[BOT] Profitto stimato: ${total:,.2f} su {len(results)} operazioni.")
        results.to_csv(OUTPUT_FILE, index=False)
        plot_profits(results)
