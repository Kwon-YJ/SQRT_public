import pandas as pd
import datetime
import ccxt
import time
import dataframe as df
import pandas_ta as ta
import numpy as np


def bb(x, w=20, k=2):  # 볼린저 밴드
    data = pd.Series(x)
    mbb = data.rolling(w).mean()
    lbb = mbb - k * data.rolling(w).std()
    ubb = mbb + k * data.rolling(w).std()
    # return [lbb.tolist()[-20:], mbb.tolist()[-20:], ubb.tolist()[-20:]]
    return [lbb.tolist()[-1], mbb.tolist()[-1], ubb.tolist()[-1]]


binance = ccxt.binance(
    {
        "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV",
        "secret": "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87",
        "enableRateLimit": True,
    }
)

# temp_list = list(binance.fetch_tickers().keys())
# temp_list = list(set(temp_list) - set(['BTCUSDT_210625', 'ETHUSDT_210625']))

temp_ohlcv = binance.fetch_ohlcv("DOGE/USDT", "1h")
atr = get_atr(temp_ohlcv, 14)
temp = [temp_ohlcv[i][4] for i in range(len(temp_ohlcv))]

changed_ohlcv = [temp_ohlcv[i][4] for i in range(len(temp_ohlcv))][:-1]
changed_ohlcv.append(temp_ohlcv[-1][4] + atr[-1] * 3)


before = bb(temp, 20, 3)
after = bb(changed_ohlcv, 20, 3)

print(before)
print(after)
