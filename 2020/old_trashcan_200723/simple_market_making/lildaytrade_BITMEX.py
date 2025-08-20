import ccxt
import time
import pandas as pd
import os
import telegram
import datetime
from pprint import pprint


def on_buy_mode(ticker):
    save_price.clear()
    price = bitmex.fetch_order_book(ticker)["bids"][1][0]
    order = bitmex.create_order(ticker, "limit", "buy", size, price, params)
    save_price.append(price)
    time.sleep(3)

    while True:
        time.sleep(0.5)
        state = bitmex.fetch_order_status(order["info"]["orderID"])
        now = int(datetime.datetime.now().second)
        if now > 3:
            continue
        if state == "closed":
            return None
        else:
            time.sleep(3)
            state = bitmex.fetch_order_status(order["info"]["orderID"])
            if state != "canceled":
                bitmex.cancel_order(order["info"]["orderID"], ticker)
            save_price.clear()
            price = bitmex.fetch_order_book(ticker)["bids"][1][0]
            order = bitmex.create_order(ticker, "limit", "buy", size, price, params)
            save_price.append(price)
            continue


def on_sell_mode(ticker):
    price = get_sell_price()
    order = bitmex.create_order(ticker, "limit", "sell", size, price, params)
    time.sleep(3)

    while True:
        time.sleep(0.5)
        state = bitmex.fetch_order_status(order["info"]["orderID"])
        now = int(datetime.datetime.now().second)
        if now > 3:
            continue
        if state == "closed":
            return None
        else:
            time.sleep(3)
            state = bitmex.fetch_order_status(order["info"]["orderID"])
            if state != "canceled":
                bitmex.cancel_order(order["info"]["orderID"], ticker)

            price = get_sell_price()
            order = bitmex.create_order(ticker, "limit", "sell", size, price, params)
            continue


def get_sell_price():
    a = save_price[0] + 3.5
    b = bitmex.fetch_order_book(ticker)["bids"][1][0]
    if a < b:
        return b
    else:
        return a - 7


"""
bitmex = ccxt.bitmex({
    'apiKey': '3pFJ5lblk8ff8brlz2plOG2o',
    'secret': 'KKFk0a-YvtW8aEcS33HbQlxJ63rHpdA95D7IWNALSOTVraB1',
    'enableRateLimit': True,
    'RateLimit' : 10000
})
bitmex.load_markets()
"""

bitmex = ccxt.bitmex(
    {
        "apiKey": "qlMFMLdQ7t2K7C4syVWS4Ia_",
        "secret": "CHAfO5s1qzAdgImnTxiGZHq07t3jc9HTs-g50KiHPGDY6xS8",
    }
)
if "test" in bitmex.urls:
    bitmex.urls["api"] = bitmex.urls["test"]  # ←----- switch the base URL to testnet

bot = telegram.Bot(token=my_token)


# save_price = []

save_price = [9575]

ticker = "BTC/USD"
time_frame = "1m"
size = 50
params = {"execInst": "ParticipateDoNotInitiate", "leverage": 5}
# params = {'leverage' : 5}
# open, canceled, closed


while True:
    on_sell_mode(ticker)
    print("테스트 시마이")
    time.sleep(300)
