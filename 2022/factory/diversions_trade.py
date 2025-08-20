from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import argrelextrema
import Utils
import pandas_ta as ta
import time


def get_target(ticker_list, timeframe):
    # print(timeframe)
    for ticker_name in ticker_list:
        Ohlcv = binance.fetch_ohlcv(ticker_name, timeframe, None, 100)
        data = pd.DataFrame(
            data=np.array(Ohlcv), columns=["Time", "Open", "High", "Low", "Close", "V"]
        )  ## rsi(15, high)
        rsi_entry = data.ta.rsi(length=14).tolist()
        data.insert(6, "rsi", rsi_entry, True)
        data = data.fillna(0)

        max_price = argrelextrema(data["Close"].values, np.greater, order=5)[0][-2:]
        min_price = argrelextrema(data["Close"].values, np.less, order=5)[0][-2:]
        max_rsi = argrelextrema(data["rsi"].values, np.greater, order=5)[0][-2:]
        min_rsi = argrelextrema(data["rsi"].values, np.less, order=5)[0][-2:]

        if len(max_price) > 1:
            max_before = data.iloc[max_price[0]]
            max_after = data.iloc[max_price[1]]
            if max_price[-1] > 97:
                if (
                    np.array_equal(max_price, max_rsi)
                    and data["rsi"][max_rsi[0]] > 80
                    and data["rsi"][max_rsi[1]] > 70
                ):
                    if (
                        max_before["rsi"] > max_after["rsi"]
                        and max_before["Close"] < max_after["Close"]
                    ):
                        # print('overbuy',ticker_name)
                        msg = f"overbuy : {ticker_name}, {timeframe}"
                        Utils.telegram_send(msg)

        if len(min_price) > 1:
            min_before = data.iloc[min_price[0]]
            min_after = data.iloc[min_price[1]]
            if min_price[-1] > 97:
                if (
                    np.array_equal(min_price, min_rsi)
                    and data["rsi"][min_rsi[0]] < 20
                    and data["rsi"][min_rsi[1]] < 30
                ):
                    if (
                        min_before["rsi"] < min_after["rsi"]
                        and min_before["Close"] > min_after["Close"]
                    ):
                        # print('oversell',ticker_name)
                        msg = f"oversell : {ticker_name}, {timeframe}"
                        Utils.telegram_send(msg)
                        # print('')


if __name__ == "__main__":
    binance = Utils.use_binance()
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
        "COMP/USDT",
        "OMG/USDT",
        "DOGE/USDT",
        "SXP/USDT",
        "KAVA/USDT",
        "BAND/USDT",
        "RLC/USDT",
        "WAVES/USDT",
        "MKR/USDT",
        "SNX/USDT",
        "DOT/USDT",
        "YFI/USDT",
        "BAL/USDT",
        "CRV/USDT",
        "TRB/USDT",
        "YFII/USDT",
        "RUNE/USDT",
        "SUSHI/USDT",
        "SRM/USDT",
        "BZRX/USDT",
        "EGLD/USDT",
        "SOL/USDT",
        "ICX/USDT",
        "STORJ/USDT",
        "BLZ/USDT",
        "UNI/USDT",
        "AVAX/USDT",
        "FTM/USDT",
        "HNT/USDT",
        "ENJ/USDT",
        "FLM/USDT",
        "TOMO/USDT",
        "REN/USDT",
        "KSM/USDT",
        "NEAR/USDT",
        "AAVE/USDT",
        "FIL/USDT",
        "RSR/USDT",
        "LRC/USDT",
        "MATIC/USDT",
        "OCEAN/USDT",
        "CVC/USDT",
        "BEL/USDT",
        "CTK/USDT",
        "AXS/USDT",
        "ALPHA/USDT",
        "ZEN/USDT",
        "SKL/USDT",
        "GRT/USDT",
        "1INCH/USDT",
        "AKRO/USDT",
        "CHZ/USDT",
        "SAND/USDT",
        "ANKR/USDT",
        "LUNA/USDT",
        "BTS/USDT",
        "LIT/USDT",
        "UNFI/USDT",
        "DODO/USDT",
        "REEF/USDT",
        "RVN/USDT",
        "SFP/USDT",
        "XEM/USDT",
        "COTI/USDT",
        "CHR/USDT",
        "MANA/USDT",
        "ALICE/USDT",
        "HBAR/USDT",
        "ONE/USDT",
        "LINA/USDT",
        "STMX/USDT",
        "DENT/USDT",
        "CELR/USDT",
        "HOT/USDT",
        "MTL/USDT",
        "OGN/USDT",
        "BTT/USDT",
        "NKN/USDT",
        "SC/USDT",
        "DGB/USDT",
        "ICP/USDT",
        "BAKE/USDT",
        "GTC/USDT",
        "KEEP/USDT",
    ]

    while 1:
        time.sleep(5)

        time_now = Utils.get_time()[1]

        # UTC 00:00
        if int(time_now) == 2357:
            get_target(ticker_list, "1d")
            get_target(ticker_list, "12h")
            get_target(ticker_list, "6h")
            get_target(ticker_list, "4h")
            get_target(ticker_list, "2h")
            get_target(ticker_list, "1h")
            get_target(ticker_list, "30m")
            get_target(ticker_list, "15m")
            time.sleep(180)
            continue

        # UTC 12:00
        if int(time_now) == 1157:
            get_target(ticker_list, "12h")
            get_target(ticker_list, "6h")
            get_target(ticker_list, "4h")
            get_target(ticker_list, "2h")
            get_target(ticker_list, "1h")
            get_target(ticker_list, "30m")
            get_target(ticker_list, "15m")
            time.sleep(180)
            continue

        # UTC 06:00, 18:00
        if int(time_now) == 558 or int(time_now) == 1758:
            get_target(ticker_list, "6h")
            get_target(ticker_list, "2h")
            get_target(ticker_list, "1h")
            get_target(ticker_list, "30m")
            get_target(ticker_list, "15m")
            time.sleep(120)
            continue

        # UTC 04:00, 08:00, 16:00, 20:00
        if (
            int(time_now) == 1558
            or int(time_now) == 1958
            or int(time_now) == 758
            or int(time_now) == 358
        ):
            get_target(ticker_list, "4h")
            get_target(ticker_list, "2h")
            get_target(ticker_list, "1h")
            get_target(ticker_list, "30m")
            get_target(ticker_list, "15m")
            time.sleep(120)
            continue

        # UTC 02:00, 10:00, 14:00, 22:00
        if (
            int(time_now) == 158
            or int(time_now) == 958
            or int(time_now) == 1358
            or int(time_now) == 2158
        ):
            get_target(ticker_list, "2h")
            get_target(ticker_list, "1h")
            get_target(ticker_list, "30m")
            get_target(ticker_list, "15m")
            time.sleep(120)
            continue

        # UTC 01:00, 03:00, 07:00, 09:00, 11:00, 13:00, 15:00, 17:00, 19:00, 21:00, 23:00
        if int(time_now[2:]) == 58:
            get_target(ticker_list, "1h")
            get_target(ticker_list, "30m")
            get_target(ticker_list, "15m")
            time.sleep(120)
            continue

        # UTC xx:30
        if int(time_now[2:]) == 29:
            get_target(ticker_list, "30m")
            get_target(ticker_list, "15m")
            time.sleep(60)
            continue

        # UTC xx:45, xx:15
        if int(time_now[2:]) == 44 or int(time_now[2:]) == 14:
            get_target(ticker_list, "15m")
            time.sleep(60)
            continue
