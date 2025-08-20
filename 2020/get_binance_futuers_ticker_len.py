import ccxt
import time
import datetime


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
binance.load_markets()

"""
a = binance.fetch_tickers().keys()


print(a)
print('')
print(len(a))
"""

import ccxt

binance = ccxt.binance()


def get_tickers(base):
    # base = '/USDT' or '/BNB' or '/BTC' or ...
    All_ticker = binance.fetch_tickers().keys()
    tickers = [s for s in All_ticker if base in s]
    result = []
    for i, item in enumerate(tickers):
        ohlcv = binance.fetch_order_book(item)
        if len(ohlcv["bids"]) != 0 and ohlcv["bids"][1][0] > 0.00002:
            result.append(item)
    return result


print("")

print("")
a = list(
    set(get_tickers("/BTC"))
    - set(["WBTC/BTC", "DIA/BTC", "NEBL/BTC", "BEAM/BTC", "PIVX/BTC"])
)

print(a)
print("")
print(len(a))

b = list(set(get_tickers("/USDT")))

print(b)
print("")
print(len(b))


a = [a[i][:-4] for i in range(len(a))]
print(a)
print("")
print(len(a))

b = [b[i][:-5] for i in range(len(b))]
print(b)
print("")
print(len(b))

c = list(set(a) & set(b))
print(c)
print("")
print(len(c))

c = [c[i] + "/BTC" for i in range(len(c))]
print(c)
print("")
print(len(c))
# 93개 조건 : if len(ohlcv['bids']) != 0 and ohlcv['bids'][1][0] > 0.00002:
# ['LEND/BTC', 'ARK/BTC', 'BCD/BTC', 'BNB/BTC', 'XMR/BTC', 'ZRX/BTC', 'ZEN/BTC', 'KMD/BTC', 'MKR/BTC', 'NMR/BTC', 'WAN/BTC', 'REN/BTC', 'WAVES/BTC', 'OCEAN/BTC', 'CRV/BTC', 'HC/BTC', 'WTC/BTC', 'NULS/BTC', 'EOS/BTC', 'BAND/BTC', 'ONT/BTC', 'ATOM/BTC', 'MDA/BTC', 'ETH/BTC', 'WNXM/BTC', 'ICX/BTC', 'BNT/BTC', 'KAVA/BTC', 'TOMO/BTC', 'REP/BTC', 'LTC/BTC', 'BAL/BTC', 'IOTA/BTC', 'YFI/BTC', 'BAT/BTC', 'NEO/BTC', 'VIA/BTC', 'BZRX/BTC', 'OMG/BTC', 'XZC/BTC', 'ALGO/BTC', 'LINK/BTC', 'GAS/BTC', 'QTUM/BTC', 'OGN/BTC', 'KNC/BTC', 'XRP/BTC', 'SNX/BTC', 'SUSHI/BTC', 'DASH/BTC', 'SRM/BTC', 'STORJ/BTC', 'TRB/BTC', 'RDN/BTC', 'LSK/BTC', 'THETA/BTC', 'PPT/BTC', 'MCO/BTC', 'BTG/BTC', 'SKY/BTC', 'FIO/BTC', 'STRAT/BTC', 'RUNE/BTC', 'COMP/BTC', 'AVA/BTC', 'NXS/BTC', 'SXP/BTC', 'DCR/BTC', 'ANT/BTC', 'PAXG/BTC', 'MTL/BTC', 'EVX/BTC', 'GVT/BTC', 'NAS/BTC', 'WBTC/BTC', 'NANO/BTC', 'XTZ/BTC', 'BEAM/BTC', 'ENG/BTC', 'KSM/BTC', 'LUNA/BTC', 'PIVX/BTC', 'SOL/BTC', 'ZEC/BTC', 'DOT/BTC', 'YFII/BTC', 'RLC/BTC', 'ETC/BTC', 'GXS/BTC', 'NEBL/BTC', 'BCH/BTC', 'FTT/BTC', 'PNT/BTC']
