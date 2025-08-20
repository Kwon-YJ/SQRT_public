import ccxt
import time
import pandas as pd
import os
import telegram
import datetime
from pprint import pprint

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

temp_time = str(datetime.datetime.now() - datetime.timedelta(hours=10.1))
convert = temp_time[:10] + "T" + temp_time[11:19]
timestamp = bitmex.parse8601(convert)

ticker = "BTC/USD"
time_frame = "1m"
status_ = [0]
size = 50

bitmex.create_order(ticker, "market", "buy", (size / 2), None, {"leverage": 5})

while True:
    now = int(datetime.datetime.now().second)
    if now > 3:
        continue

    try:
        bitmex.cancel_order(order["info"]["orderID"], ticker)
        time.sleep(1)
    except:
        if status_[0] == 0:
            status_[0] = 1
        else:
            status_[0] = 0

    ohlcv = bitmex.fetch_ohlcv(ticker, time_frame, timestamp)

    long_target = ohlcv[-2][2]
    short_target = ohlcv[-2][3]
    current_price = ohlcv[-1][4]

    if status_[0] == 1:
        order = bitmex.create_order(
            ticker, "limit", "sell", size, short_target, {"leverage": 5}
        )
    elif status_[0] == 0:
        order = bitmex.create_order(
            ticker, "limit", "buy", size, long_target, {"leverage": 5}
        )

    time.sleep(35)
