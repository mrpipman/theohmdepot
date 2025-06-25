# Energy Nodal Arbitrage Bot

Questo bot effettua operazioni di arbitraggio su mercati energetici (PJM, NYISO, ISO-NE) sfruttando differenze di prezzo nei nodi elettrici.

## Features
- Scarica dati pubblici più recenti
- Calcola spread e ROI per operazioni
- Telegram alert + grafico performance
- Whitelist nodi affidabili
- Reinvestimento dei profitti

## Avvio
```
pip install pandas matplotlib requests
python arbitrage_bot_full.py
```

## Pianificazione (Scheduler)
Puoi schedularlo ogni giorno con `cron` o `Task Scheduler`.

Esempio (Linux):
```
0 13 * * * /usr/bin/python3 /path/to/arbitrage_bot_full.py
```
