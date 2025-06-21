# src/utils/fmp.py
import requests
import functools
import os
from dotenv import load_dotenv
load_dotenv()  # 👈 carga variables del .env

import os
API_KEY = os.getenv("FMP_API_KEY", "demo")  # Usa demo si no está definida
 # Usa tu API Key real aquí

BASE_URL = "https://financialmodelingprep.com/api/v3"

def fetch_fmp(endpoint, params=None):
    if params is None:
        params = {}
    params["apikey"] = API_KEY
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

@functools.lru_cache(maxsize=128)
def get_ratios(ticker):
    return fetch_fmp(f"ratios-ttm/{ticker}")

@functools.lru_cache(maxsize=128)
def get_profile(ticker):
    return fetch_fmp(f"profile/{ticker}")

@functools.lru_cache(maxsize=128)
def get_income_statement(ticker):
    return fetch_fmp(f"income-statement/{ticker}", {"limit": 4})

@functools.lru_cache(maxsize=128)
def get_balance_sheet(ticker):
    return fetch_fmp(f"balance-sheet-statement/{ticker}", {"limit": 4})
