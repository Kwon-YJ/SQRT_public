# -*- coding: utf-8 -*-
import ccxt
import time
from pprint import pprint
import pandas as pd
import datetime
import telegram

bot = telegram.Bot(token=my_token)

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


def get_time(temp):
    now = temp
    YYYY = str(now.year)
    MM = str(now.month)
    DD = str(now.day)
    hh = str(now.hour)
    mm = str(now.minute)

    if len(MM) != 2:
        MM = "0" + MM
    if len(DD) != 2:
        DD = "0" + DD
    if len(hh) != 2:
        hh = "0" + hh
    if len(mm) != 2:
        mm = "0" + mm

    return YYYY + MM + DD, hh + mm


status = 0
while True:
    try:
        time.sleep(140)
        ohlcv = binance.fetch_ohlcv("BTC/USDT", "1h")[-50:]
        ha_ohlcv = []
        for i in range(1, len(ohlcv)):
            if i == 1:
                ha_open = (ohlcv[i - 1][1] + ohlcv[i - 1][4]) / 2
            else:
                ha_open = (ha_ohlcv[i - 2][1] + ha_ohlcv[i - 2][4]) / 2
            timestamp = ohlcv[i][0]
            ha_close = (ohlcv[i][1] + ohlcv[i][2] + ohlcv[i][3] + ohlcv[i][4]) / 4
            ha_high = max(ohlcv[i][2], ha_close, ha_open)
            ha_low = min(ohlcv[i][3], ha_close, ha_open)
            ha_ohlcv.append(
                [
                    timestamp,
                    round(ha_open, 2),
                    round(ha_high, 2),
                    round(ha_low, 2),
                    round(ha_close, 2),
                ]
            )
        # 롱 = 현재자산 * (진입가격 / 청산가격)
        # 숏 = 현재자산 * (청산가격 / 진입가격)
        result = []
        for i in range(len(ha_ohlcv)):
            if ha_ohlcv[i][1] > ha_ohlcv[i][4]:
                result.append("red")
            elif ha_ohlcv[i][1] < ha_ohlcv[i][4]:
                result.append("green")

        start = get_time(datetime.datetime.now())[1][-2:]
        if int(start) < 5:
            if result[-2] == "red" and result[-2] != result[-3] and status >= 0:
                # short
                if status == 0:
                    amount = 0.002
                    status = status - 1
                else:
                    amount = 0.004
                    status = status - 2
                order = binance.create_order(
                    "BTC/USDT", "market", "sell", amount, None, {"leverage": 1}
                )
                time.sleep(300)

            elif result[-2] == "green" and result[-2] != result[-3] and status <= 0:
                # long
                if status == 0:
                    amount = 0.002
                    status = status + 1
                else:
                    amount = 0.004
                    status = status + 2
                order = binance.create_order(
                    "BTC/USDT", "market", "buy", amount, None, {"leverage": 1}
                )
                time.sleep(300)
    except:
        bot.send_message(chat_id=801167350, text="하이킨아시 에러")
        time.sleep(140)
        continue
