# ⚡ The Ω Depot

> Dashboard professionale per analisi e automazione del trading su **LMP arbitrage**

![Logo](logo.png)

---

## 🚀 Funzionalità principali

- **📊 KPI dinamici**: ROI medio, profitto totale, Sharpe ratio, drawdown
- **📈 Grafici interattivi**: ROI cumulato, distribuzioni, cluster, heatmap
- **📤 Esportazione CSV** dei trade filtrati
- **📬 Integrazione Telegram** per alert e invio report PDF
- **🧪 Simulazione Backtest** giornaliero
- **🧠 Suggerimenti insight + Top nodi da monitorare**

---

## 🧰 Requisiti

- Python 3.9+
- vedi `requirements.txt` per le dipendenze

Installa con:

```bash
pip install -r requirements.txt
```

---

## ▶️ Avvio locale

```bash
streamlit run dashboard_streamlit.py
```

---

## 🌐 Deploy con Streamlit Cloud

1. Vai su [streamlit.io/cloud](https://streamlit.io/cloud)
2. Clicca “New app”
3. Seleziona il repo `mrpipman/theohmdepot`
4. File principale: `dashboard_streamlit.py`
5. Clicca **Deploy**

---

## 📬 Notifiche Telegram

Questo progetto invia alert con ROI > soglia e report PDF con:

```bash
python send_report_telegram.py
```

Per attivare:
- Modifica `send_report_telegram.py` con il tuo **bot token** e **chat ID**
- Pianifica con `cron` o `Task Scheduler` per invio giornaliero

---

## 🧠 Note

Creato con ❤️ per chi fa arbitraggio LMP come un vero Ωperatore.

---

---

## 🌍 Live App

👉 [Apri su Streamlit Cloud](https://theohmdepot.streamlit.app) *(link demo modificabile)*

---

## 🛠 Cron Job Telegram

Esegui lo script ogni giorno alle 6:00 UTC:

```bash
0 6 * * * /usr/bin/python3 /percorso/send_report_telegram.py
```

