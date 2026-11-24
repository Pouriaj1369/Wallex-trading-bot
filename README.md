import json
import urllib.request

url = "https://api.wallex.ir/hector/web/v1/markets"

with urllib.request.urlopen(url) as r:
    data = json.loads(r.read())

markets = data["result"]["markets"]

for coin in ["BTC", "ETH", "XRP"]:
    market = next(m for m in markets if m["symbol"] == coin + "TMN")
    print(coin, market["price"])
