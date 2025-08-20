import ccxt
import time

exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.load_markets()

while True:
    time.sleep(3600)
    today_money = binance.fetch_balance()["BNB"]["free"]
    # today_money 타입 확인
    if today_money < 1:
        binance.create_order("BNB/USDT", "market", "buy", 1)
