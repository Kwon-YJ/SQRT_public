from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from scipy.signal import argrelextrema
import Utils
import pandas_ta as ta


def get_target(ticker_name, timeframe):
    # Ohlcv = binance.fetch_ohlcv(ticker_name, timeframe, None, 100)
    Ohlcv = Utils.bithumb.fetch_ohlcv(ticker_name, timeframe, None, 100)

    data = pd.DataFrame(
        data=np.array(Ohlcv), columns=["Time", "Open", "High", "Low", "Close", "V"]
    )  ## rsi(15, high)
    rsi_entry = data.ta.rsi(length=14).tolist()

    if rsi_entry[-1] > 30 and rsi_entry[-1] < 70:
        return None

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
            # if np.array_equal(max_price,max_rsi):
            if (
                np.array_equal(max_price, max_rsi)
                and data["rsi"][max_rsi[0]] > 80
                and data["rsi"][max_rsi[1]] > 70
            ):
                if (
                    max_before["rsi"] > max_after["rsi"]
                    and max_before["Close"] < max_after["Close"]
                ):
                    print("overbuy", ticker_name)

    if len(min_price) > 1:
        min_before = data.iloc[min_price[0]]
        min_after = data.iloc[min_price[1]]
        if min_price[-1] > 97:
            # if np.array_equal(min_price,min_rsi):
            if (
                np.array_equal(min_price, min_rsi)
                and data["rsi"][min_rsi[0]] < 20
                and data["rsi"][min_rsi[1]] < 30
            ):
                if (
                    min_before["rsi"] < min_after["rsi"]
                    and min_before["Close"] > min_after["Close"]
                ):
                    print("oversell", ticker_name)
                    print("")


import time

if __name__ == "__main__":
    # ticker_list = list(Utils.bithumb.fetch_tickers().keys())
    ticker_list = [
        "BTC/KRW",
        "ETH/KRW",
        "LTC/KRW",
        "ETC/KRW",
        "XRP/KRW",
        "BCH/KRW",
        "QTUM/KRW",
        "BTG/KRW",
        "EOS/KRW",
        "ICX/KRW",
        "TRX/KRW",
        "ELF/KRW",
        "OMG/KRW",
        "KNC/KRW",
        "GLM/KRW",
        "ZIL/KRW",
        "WAXP/KRW",
        "POWR/KRW",
        "LRC/KRW",
        "STEEM/KRW",
        "STRAX/KRW",
        "ZRX/KRW",
        "REP/KRW",
        "XEM/KRW",
        "SNT/KRW",
        "ADA/KRW",
        "CTXC/KRW",
        "BAT/KRW",
        "WTC/KRW",
        "THETA/KRW",
        "LOOM/KRW",
        "WAVES/KRW",
        "TRUE/KRW",
        "LINK/KRW",
        "ENJ/KRW",
        "VET/KRW",
        "MTL/KRW",
        "IOST/KRW",
        "TMTG/KRW",
        "QKC/KRW",
        "ATOLO/KRW",
        "AMO/KRW",
        "BSV/KRW",
        "ORBS/KRW",
        "TFUEL/KRW",
        "VALOR/KRW",
        "CON/KRW",
        "ANKR/KRW",
        "MIX/KRW",
        "CRO/KRW",
        "FX/KRW",
        "CHR/KRW",
        "MBL/KRW",
        "MXC/KRW",
        "FCT/KRW",
        "TRV/KRW",
        "DAD/KRW",
        "WOM/KRW",
        "SOC/KRW",
        "BOA/KRW",
        "FLETA/KRW",
        "SXP/KRW",
        "COS/KRW",
        "APIX/KRW",
        "EL/KRW",
        "BASIC/KRW",
        "HIVE/KRW",
        "XPR/KRW",
        "VRA/KRW",
        "FIT/KRW",
        "EGG/KRW",
        "BORA/KRW",
        "ARPA/KRW",
        "CTC/KRW",
        "APM/KRW",
        "CKB/KRW",
        "AERGO/KRW",
        "ANW/KRW",
        "CENNZ/KRW",
        "EVZ/KRW",
        "CYCLUB/KRW",
        "SRM/KRW",
        "QTCON/KRW",
        "UNI/KRW",
        "YFI/KRW",
        "UMA/KRW",
        "AAVE/KRW",
        "COMP/KRW",
        "REN/KRW",
        "BAL/KRW",
        "RSR/KRW",
        "NMR/KRW",
        "RLC/KRW",
        "UOS/KRW",
        "SAND/KRW",
        "GOM2/KRW",
        "RINGX/KRW",
        "BEL/KRW",
        "OBSR/KRW",
        "ORC/KRW",
        "POLA/KRW",
        "AWO/KRW",
        "ADP/KRW",
        "DVI/KRW",
        "GHX/KRW",
        "MIR/KRW",
        "MVC/KRW",
        "BLY/KRW",
        "WOZX/KRW",
        "ANV/KRW",
        "GRT/KRW",
        "MM/KRW",
        "BIOT/KRW",
        "XNO/KRW",
        "SNX/KRW",
        "SOFI/KRW",
        "COLA/KRW",
        "NU/KRW",
        "OXT/KRW",
        "LINA/KRW",
        "MAP/KRW",
        "AQT/KRW",
        "WIKEN/KRW",
        "CTSI/KRW",
        "MANA/KRW",
        "LPT/KRW",
        "MKR/KRW",
        "SUSHI/KRW",
        "ASM/KRW",
        "PUNDIX/KRW",
        "CELR/KRW",
        "LF/KRW",
        "ARW/KRW",
        "FRONT/KRW",
        "MSB/KRW",
        "RLY/KRW",
        "OCEAN/KRW",
        "BFC/KRW",
        "ALICE/KRW",
        "COTI/KRW",
        "CAKE/KRW",
        "BNT/KRW",
        "XVS/KRW",
        "CHZ/KRW",
        "AXS/KRW",
        "DAO/KRW",
        "DAI/KRW",
        "MATIC/KRW",
        "WOO/KRW",
        "BAKE/KRW",
        "VELO/KRW",
        "BCD/KRW",
        "XLM/KRW",
        "GXC/KRW",
        "VSYS/KRW",
        "IPX/KRW",
        "WICC/KRW",
        "ONT/KRW",
        "LUNA/KRW",
        "AION/KRW",
        "META/KRW",
        "KLAY/KRW",
        "ONG/KRW",
        "ALGO/KRW",
        "JST/KRW",
        "XTZ/KRW",
        "MLK/KRW",
        "WEMIX/KRW",
        "DOT/KRW",
        "ATOM/KRW",
        "SSX/KRW",
        "TEMCO/KRW",
        "HIBS/KRW",
        "BURGER/KRW",
        "DOGE/KRW",
        "KSM/KRW",
        "CTK/KRW",
        "XYM/KRW",
        "BNB/KRW",
        "NFT/KRW",
        "SUN/KRW",
        "XEC/KRW",
        "PCI/KRW",
        "SOL/KRW",
        "C98/KRW",
        "MED/KRW",
        "1INCH/KRW",
        "BOBA/KRW",
        "GALA/KRW",
        "BTT/KRW",
    ]

    a = datetime.now()

    print(len(ticker_list))

    print("30m")
    for ticker in ticker_list:
        try:
            get_target(ticker, "30m")
        except:
            time.sleep(0.3)
            continue

    print("1h")
    for ticker in ticker_list:
        try:
            get_target(ticker, "1h")
        except:
            time.sleep(0.3)
            continue

    print("6h")
    for ticker in ticker_list:
        try:
            get_target(ticker, "6h")
        except:
            time.sleep(0.3)
            continue

    print("12h")
    for ticker in ticker_list:
        try:
            get_target(ticker, "12h")
        except:
            time.sleep(0.3)
            continue

    print("1d")
    for ticker in ticker_list:
        try:
            get_target(ticker, "1d")
        except:
            time.sleep(0.3)
            continue

    print(datetime.now() - a)
