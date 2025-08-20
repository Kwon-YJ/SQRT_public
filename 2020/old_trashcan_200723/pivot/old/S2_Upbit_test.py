import ccxt
import time


upbit = ccxt.upbit(
    {
        "apiKey": "3pFJ5lblk8ff8brlz2plOG2o",
        "secret": "KKFk0a-YvtW8aEcS33HbQlxJ63rHpdA95D7IWNALSOTVraB1",
        "enableRateLimit": True,
        "RateLimit": 10000,
    }
)
upbit.load_markets()


temp = upbit.fetch_tickers().keys()

tickers = [s for s in temp if "KRW" in s]

day = 1

time_frame = "1d"
for i, item in enumerate(tickers):
    time.sleep(1)
    ohlcv = upbit.fetch_ohlcv(item, time_frame)
