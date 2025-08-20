import ccxt
import time
import operator

exchange_class = getattr(ccxt, "binance")
binance = exchange_class(
    {
        "urls": {
            "api": {
                "public": "https://fapi.binance.com/fapi/v1",
                "private": "https://fapi.binance.com/fapi/v1",
            },
        }
    }
)
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()


# IBS = close - low / high - low

ticker_list = [
    "BTC/USDT",
    "ETH/USDT",
    "BCH/USDT",
    "XRP/USDT",
    "EOS/USDT",
    "LTC/USDT",
    "TRX/USDT",
    "ETC/USDT",
    "LINK/USDT",
    "XLM/USDT",
    "ADA/USDT",
    "XMR/USDT",
    "DASH/USDT",
    "ZEC/USDT",
    "XTZ/USDT",
    "BNB/USDT",
    "ATOM/USDT",
    "ONT/USDT",
    "IOTA/USDT",
    "BAT/USDT",
    "VET/USDT",
    "NEO/USDT",
    "QTUM/USDT",
    "IOST/USDT",
    "THETA/USDT",
    "ALGO/USDT",
    "ZIL/USDT",
    "KNC/USDT",
    "ZRX/USDT",
]


def temp_func(day, times):
    result = {}
    for i in range(len(ticker_list)):
        try:
            ohlcv = binance.fetch_ohlcv(ticker_list[i], "1d")
            temp = (ohlcv[-day - 1][4] - ohlcv[-day - 1][3]) / (
                ohlcv[-day - 1][2] - ohlcv[-day - 1][3]
            )
            result[ticker_list[i]] = temp
        except:
            continue

    # Sresult= sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    Sresult = sorted(result.items(), key=operator.itemgetter(1), reverse=False)
    temp = 0
    for i in range(times):
        time_frame = "1d"
        ticker_name = Sresult[i][0]
        ohlcv = binance.fetch_ohlcv(ticker_name, time_frame)
        buy_price = ohlcv[-day][1]
        sell_price = ohlcv[-day][4]

        # print('buy :',buy_price, " sell :", sell_price)
        earning = round(-100 + buy_price / sell_price * 99.9, 5)
        temp += earning
        # print(earning)
    print("day:", day, "earning = ", temp)


"""

for i in range(2,30):
    temp_func(i, 3)
"""

a = list(binance.fetch_tickers().keys())

print(a)
