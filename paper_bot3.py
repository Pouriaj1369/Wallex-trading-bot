import json
import os
import urllib.request

URL = "https://api.wallex.ir/hector/web/v1/markets"
STATE_FILE = "paper_state.json"

INITIAL_USDT = 17
COINS = ["BTC", "ETH", "XRP"]
BUY_DROP = 0.01
SELL_RISE = 0.015

with urllib.request.urlopen(URL, timeout=20) as response:
    data = json.loads(response.read())

markets = data["result"]["markets"]

def get_price(symbol):
    market = next(
        m for m in markets if m["symbol"] == symbol
    )
    return float(market["price"])

usdt_price = get_price("USDTTMN")
prices = {
    coin: get_price(coin + "TMN")
    for coin in COINS
}

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
else:
    total_tmn = INITIAL_USDT * usdt_price
    allocation = total_tmn / len(COINS)

    state = {
        "initial_usdt": INITIAL_USDT,
        "coins": {
            coin: {
                "cash": allocation,
                "quantity": 0.0,
                "buy_price": None,
                "reference": prices[coin]
            }
            for coin in COINS
        }
    }

for coin in COINS:
    item = state["coins"][coin]
    price = prices[coin]

    if item["quantity"] == 0:
        if price <= item["reference"] * (1 - BUY_DROP):
            item["quantity"] = item["cash"] / price
            item["cash"] = 0.0
            item["buy_price"] = price
            print(coin, "PAPER BUY", price)
        else:
            print(coin, "WAITING", price)

    elif price >= item["buy_price"] * (1 + SELL_RISE):
        item["cash"] = item["quantity"] * price
        item["quantity"] = 0.0
        item["buy_price"] = None
        item["reference"] = price
        print(coin, "PAPER SELL", price)

    else:
        print(coin, "HOLD", price)

total_value = 0.0

for coin in COINS:
    item = state["coins"][coin]
    total_value += item["cash"]
    total_value += item["quantity"] * prices[coin]

print("Total value in USDT:", round(total_value / usdt_price, 4))
print("Paper trading only. No real orders.")

with open(STATE_FILE, "w") as f:
    json.dump(state, f, indent=2)
