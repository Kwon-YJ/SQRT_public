# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import urllib.request
import json
import pandas as pd
import numpy as np

# from pandas.core.indexing import convert_missing_indexer
import pandas_ta
import parmap


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={str(limit)}"  # monitoring
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        output = json.loads(text_data)
    except Exception as e:
        # print(e, '\n', 'ccxt.base.errors.BadSymbol: binance does not have market symbol {0}'.format(ticker))
        return None
    output = [list(map(float, output[i])) for i in range(len(output))]
    return output


binance = ccxt.binance(
    {
        "options": {"defaultType": "future"},
        "timeout": 30000,
        # "apiKey":"f6LEy0POPdaukqwlrnC4KvJbGWkcXRfVmKbsPmFAaPlyL2Rytswf7ilTa3kAjnQh",
        # "secret": "sLvrd7ZT6c49yZVlnFRhPvJcIg8z39S6dVwZcIfPhFueA5BAy5UpTT3ZbVZg9zA2",
        "enableRateLimit": False,
    }
)
binance.load_markets()

# ticker_list = ['BAKE/USDT', 'NKN/USDT', 'XEM/USDT', 'LRC/USDT', 'ZEC/USDT', 'LINA/USDT', 'YFI/USDT', 'RVN/USDT', 'QTUM/USDT', 'SXP/USDT', 'CVC/USDT', 'CHZ/USDT', 'REEF/USDT', 'FIL/USDT', 'MTL/USDT', 'XRP/USDT', 'MATIC/USDT', 'COTI/USDT', 'NEO/USDT', 'ALGO/USDT', 'HBAR/USDT', 'BAT/USDT', 'REN/USDT', 'ADA/USDT', 'AVAX/USDT', 'HOT/USDT', 'TRX/USDT', 'AXS/USDT', 'AKRO/USDT', 'SC/USDT', 'ALPHA/USDT', 'KNC/USDT', 'CHR/USDT', 'AUDIO/USDT', 'XTZ/USDT', 'KSM/USDT', 'BTS/USDT', 'HNT/USDT', 'DASH/USDT', 'ICP/USDT', 'DGB/USDT', 'DOGE/USDT', 'VET/USDT', 'AAVE/USDT', 'IOTX/USDT', 'SRM/USDT', 'ONE/USDT', 'RLC/USDT', 'NEAR/USDT', 'GTC/USDT', 'STORJ/USDT', 'EGLD/USDT', 'WAVES/USDT', 'ETH/USDT', '1INCH/USDT', 'EOS/USDT', 'LUNA/USDT', 'UNFI/USDT', 'SUSHI/USDT', 'RSR/USDT', 'OMG/USDT', 'IOTA/USDT', 'DODO/USDT', 'CRV/USDT', 'ICX/USDT', 'ALICE/USDT', 'OGN/USDT', 'RAY/USDT', 'BCH/USDT', 'FTM/USDT', 'BLZ/USDT', 'BNB/USDT', 'KAVA/USDT', 'SKL/USDT', 'SOL/USDT', 'OCEAN/USDT', 'BTC/USDT', 'BTCDOM/USDT', 'LINK/USDT', 'SAND/USDT', 'ZRX/USDT', 'C98/USDT', 'XLM/USDT', 'ANKR/USDT', 'MANA/USDT', 'TRB/USDT', 'BTT/USDT', 'THETA/USDT', 'UNI/USDT', 'STMX/USDT', 'KEEP/USDT', 'IOST/USDT', 'BAND/USDT', 'ETC/USDT', 'ZIL/USDT', 'ENJ/USDT', 'LTC/USDT', 'BZRX/USDT', 'RUNE/USDT', 'CTK/USDT', 'LIT/USDT', 'SFP/USDT', 'ATOM/USDT', 'ZEN/USDT', 'TOMO/USDT', 'YFII/USDT', 'DEFI/USDT', 'FLM/USDT', 'BEL/USDT', 'COMP/USDT', 'ONT/USDT', '1000SHIB/USDT', 'TLM/USDT', 'DOT/USDT', 'GRT/USDT', 'XMR/USDT', 'MKR/USDT', 'CELR/USDT', 'BAL/USDT', 'DENT/USDT', 'SNX/USDT']
ticker_list = ["XRP/USDT"]

ticker_list = list(set(ticker_list))

today = []


for item in ticker_list:
    # item = 'BTC/USDT'
    print(item)

    ohlcvs = get_ohlcv(item, "1d", 200)

    win = 0
    lose = 0

    for ohlcv in ohlcvs:
        if ohlcv[1] < ohlcv[4]:
            win += 1
        elif ohlcv[1] > ohlcv[4]:
            lose += 1

    print(f"total : {win + lose}")
    print(f"winrate : {round(win / (win + lose) * 100, 2)}%")
    print(f"win : {win}")
    print(f"lose : {lose}")

    print("")

    new_win = 0
    new_lose = 0

    for i in range(len(ohlcvs) - 1):
        if ohlcvs[i][1] > ohlcvs[i][4]:
            if ohlcvs[i + 1][1] < ohlcvs[i + 1][4]:
                new_win += 1
            elif ohlcvs[i + 1][1] > ohlcvs[i + 1][4]:
                new_lose += 1

    print(f"total : {new_win + new_lose}")
    print(f"winrate : {round(new_win / (new_win + new_lose) * 100, 2)}%")
    print(f"new_win : {new_win}")
    print(f"new_lose : {new_lose}")

    print("")
    exit()


"""

for item in ticker_list:
    ohlcvs = get_ohlcv(item, '1d', 1400)

    if ohlcvs[-2][1] < ohlcvs[-2][4]:
            today.append(item)

print(len(today))
print(today)
"""
