import json
import urllib.request

INITIAL_BALANCE = 10.0
TRADE_AMOUNT = 1.0

URL = "https://api.wallex.ir/hector/web/v1/markets"

with urllib.request.urlopen(URL) as response:
    data = json.loads(response.read())

markets = data["result"]["markets"]

btc = next(m for m in markets if m["symbol"] == "BTCTMN")
price = float(btc["price"])

print("BTC price:", price)
print("Initial paper balance:", INITIAL_BALANCE)
print("Trade amount:", TRADE_AMOUNT)
print("Paper trading mode: ON")
print("No real orders will be placed.")
