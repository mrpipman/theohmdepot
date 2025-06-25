
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from io import StringIO

def fetch_entsoe_day_ahead_price(area='10YIT-GRTN-----B', start='20240601', end='20240602', api_key='YOUR_API_KEY'):
    url = (
        "https://web-api.tp.entsoe.eu/api?"
        f"documentType=A44&in_Domain={area}&out_Domain={area}"
        f"&periodStart={start}0000&periodEnd={end}0000&securityToken={api_key}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"ENTSO-E API Error: {response.status_code}")
    root = ET.fromstring(response.content)
    prices = []
    for time_series in root.findall(".//{*}TimeSeries"):
        period = time_series.find(".//{*}Period")
        dt = period.find(".//{*}timeInterval/{*}start").text[:10]
        for point in period.findall(".//{*}Point"):
            pos = int(point.find("{*}position").text)
            price = float(point.find("{*}price.amount").text)
            prices.append({"date": dt, "hour": pos, "price": price})
    df = pd.DataFrame(prices)
    return df

def fetch_pjm_prices():
    url = "https://dataminer2.pjm.com/feed/hrl_lmp_da/definition"
    meta = requests.get(url).json()
    if "columns" not in meta:
        raise Exception("PJM API not accessible")
    # NOTE: this function needs a separate token-free JSON endpoint for real values.
    return pd.DataFrame(meta["columns"])

def parse_nordpool_csv(csv_content):
    df = pd.read_csv(StringIO(csv_content), sep=";")
    df.columns = [col.strip() for col in df.columns]
    df = df.rename(columns={"Spot Price EUR/MWh": "price", "HourUTC": "hour", "Date": "date"})
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])
    return df

# Simulazione fetch CSV da URL pubblico (Nord Pool)
def fetch_nordpool_example_csv():
    example_url = "https://www.nordpoolgroup.com/4a7816/globalassets/marketdata-examples/elspot-prices_2023.csv"
    r = requests.get(example_url)
    return parse_nordpool_csv(r.text)
