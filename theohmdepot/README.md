
# 🔮 The Ω Depot

[![Streamlit App](https://img.shields.io/badge/Streamlit-LiveApp-ff4b4b)](https://share.streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

> Decision intelligence platform for backtesting and ROI analysis across energy nodes.

---

![demo](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmdsNjc1azllNGw4ZXdzZ2FuYzR4M2oyNWNnM3poNzgyb25reGdzZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/1dMN8cXffC96Pi6Wlt/giphy.gif)

## 🚀 Features

- 📊 ROI Dashboard: charts, KPIs, heatmaps
- 🔁 Daily automation: Telegram alerts, backup, report
- 🧠 Node clustering and backtest simulation
- 🔐 Token-based access + Demo mode
- ☁️ Easy deploy on Streamlit Cloud

## 📦 Structure

```
├── app.py
├── pages/
├── utils/
├── scripts/
├── assets/
├── backups/
├── arbitrage_trades.db
├── requirements.txt
```

## 🛠 Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🔐 Secrets

Edit `.streamlit/secrets.toml`:

```toml
access_token = "your-access-token"
demo = false
```

## 📜 License

MIT License © 2025 The Ω Depot Team
