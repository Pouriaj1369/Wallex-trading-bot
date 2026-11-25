import json
import os
import urllib.request

INITIAL_BALANCE = 10.0
TRADE_AMOUNT = 1.0

URL = "https://api.wallex.ir/hector/web/v1/markets"

with urllib.request.urlopen(URL) as response:
    data = json.loads(response.read())

markets = data["result"]["markets"]

balance = INITIAL_BALANCE
coin = None
buy_price = 0

for market in markets:
    if market["symbol"] == "BTCTMN":
        price = float(market["price"])
        break

print("BTC price:", price)
print("Paper balance:", balance, "USD")
print("Paper trading mode: ON")
print("No real orders will be placed.")
