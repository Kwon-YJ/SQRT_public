import ccxt
import time


upbit = ccxt.upbit(
    {
        "enableRateLimit": True,
        "RateLimit": 10000,
    }
)
upbit.load_markets()


temp = upbit.fetch_tickers().keys()

tickers = [s for s in temp if "KRW" in s]

day = 2

time_frame = "1d"