# -*- coding: utf-8 -*-
import ccxt
import time
import telegram

bitmex = ccxt.bitmex(
    {
        "apiKey": "3pFJ5lblk8ff8brlz2plOG2o",
        "secret": "KKFk0a-YvtW8aEcS33HbQlxJ63rHpdA95D7IWNALSOTVraB1",
        "enableRateLimit": True,
        "RateLimit": 10000,
    }
)
bot = telegram.Bot(token=my_token)

symbol = "BTC/USD"
size = 25

while True:
    try:
        data = bitmex.fetch_order_book(symbol)
        target_ask = data["asks"][2][0]
        target_bid = data["bids"][2][0]
        order2 = bitmex.create_order(
            symbol, "limit", "buy", size, target_bid, {"leverage": 5}
        )
        order1 = bitmex.create_order(
            symbol, "limit", "sell", size, target_ask, {"leverage": 5}
        )
        time.sleep(144)
    except Exception as ex:
        bot.send_message(chat_id=801167350, text=str(ex))
        time.sleep(5)
        continue
