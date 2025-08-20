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
    Ohlcv = Utils.upbit.fetch_ohlcv(ticker_name, timeframe, None, 100)

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


if __name__ == "__main__":

    a = datetime.now()

    # ticker_list = list(Utils.upbit.fetch_tickers().keys())
    ticker_list = [
        "1INCH/BTC",
        "AAVE/BTC",
        "ADA/BTC",
        "AERGO/BTC",
        "AHT/BTC",
        "ALGO/BTC",
        "ANKR/BTC",
        "AQT/BTC",
        "ARDR/BTC",
        "ARK/BTC",
        "ATOM/BTC",
        "AUCTION/BTC",
        "AUDIO/BTC",
        "AXS/BTC",
        "BASIC/BTC",
        "BAT/BTC",
        "BCH/BTC",
        "BFC/BTC",
        "BNT/BTC",
        "BORA/BTC",
        "BSV/BTC",
        "CBK/BTC",
        "CELO/BTC",
        "CHR/BTC",
        "CHZ/BTC",
        "COMP/BTC",
        "CRO/BTC",
        "CRV/BTC",
        "CTC/BTC",
        "CTSI/BTC",
        "CVC/BTC",
        "DAD/BTC",
        "DAI/BTC",
        "DAWN/BTC",
        "DENT/BTC",
        "DGB/BTC",
        "DKA/BTC",
        "DNT/BTC",
        "DOGE/BTC",
        "DOT/BTC",
        "ELF/BTC",
        "ENJ/BTC",
        "EOS/BTC",
        "ETC/BTC",
        "ETH/BTC",
        "FCT2/BTC",
        "FIL/BTC",
        "FLOW/BTC",
        "FOR/BTC",
        "FX/BTC",
        "GLM/BTC",
        "GO/BTC",
        "GRS/BTC",
        "GRT/BTC",
        "GTC/BTC",
        "HBD/BTC",
        "HIVE/BTC",
        "HUM/BTC",
        "HUNT/BTC",
        "INJ/BTC",
        "IOST/BTC",
        "IOTX/BTC",
        "IQ/BTC",
        "JST/BTC",
        "JUV/BTC",
        "KAVA/BTC",
        "LINA/BTC",
        "LINK/BTC",
        "LOOM/BTC",
        "LPT/BTC",
        "LRC/BTC",
        "LSK/BTC",
        "LTC/BTC",
        "LUNA/BTC",
        "MANA/BTC",
        "MARO/BTC",
        "MASK/BTC",
        "MATIC/BTC",
        "MED/BTC",
        "META/BTC",
        "MFT/BTC",
        "MKR/BTC",
        "MLK/BTC",
        "MOC/BTC",
        "MTL/BTC",
        "MVL/BTC",
        "NEAR/BTC",
        "NKN/BTC",
        "NMR/BTC",
        "NU/BTC",
        "OBSR/BTC",
        "OCEAN/BTC",
        "OGN/BTC",
        "OMG/BTC",
        "ONIT/BTC",
        "ORBS/BTC",
        "OXT/BTC",
        "PCI/BTC",
        "PLA/BTC",
        "POLY/BTC",
        "POWR/BTC",
        "PROM/BTC",
        "PSG/BTC",
        "PUNDIX/BTC",
        "QTCON/BTC",
        "QTUM/BTC",
        "REP/BTC",
        "RFR/BTC",
        "RLC/BTC",
        "RSR/BTC",
        "RVN/BTC",
        "SAND/BTC",
        "SBD/BTC",
        "SC/BTC",
        "SNT/BTC",
        "SNX/BTC",
        "SOL/BTC",
        "SOLVE/BTC",
        "SRM/BTC",
        "SSX/BTC",
        "STEEM/BTC",
        "STMX/BTC",
        "STORJ/BTC",
        "STPT/BTC",
        "STRAX/BTC",
        "STRK/BTC",
        "STX/BTC",
        "SUN/BTC",
        "SXP/BTC",
        "Tokamak Network/BTC",
        "TRX/BTC",
        "TUSD/BTC",
        "UNI/BTC",
        "UPP/BTC",
        "USDP/BTC",
        "VAL/BTC",
        "VET/BTC",
        "WAVES/BTC",
        "WAXP/BTC",
        "WEMIX/BTC",
        "XEM/BTC",
        "XLM/BTC",
        "XRP/BTC",
        "XTZ/BTC",
        "YGG/BTC",
        "ZIL/BTC",
        "ZRX/BTC",
        "1INCH/KRW",
        "AAVE/KRW",
        "ADA/KRW",
        "AERGO/KRW",
        "AHT/KRW",
        "ALGO/KRW",
        "ANKR/KRW",
        "AQT/KRW",
        "ARDR/KRW",
        "ARK/KRW",
        "ATOM/KRW",
        "AXS/KRW",
        "BAT/KRW",
        "BCH/KRW",
        "BORA/KRW",
        "BSV/KRW",
        "BTC/KRW",
        "BTG/KRW",
        "BTT/KRW",
        "CBK/KRW",
        "CHZ/KRW",
        "CRE/KRW",
        "CRO/KRW",
        "CVC/KRW",
        "DAWN/KRW",
        "DKA/KRW",
        "DOGE/KRW",
        "DOT/KRW",
        "ELF/KRW",
        "ENJ/KRW",
        "EOS/KRW",
        "ETC/KRW",
        "ETH/KRW",
        "FCT2/KRW",
        "FLOW/KRW",
        "GAS/KRW",
        "GLM/KRW",
        "GRS/KRW",
        "HBAR/KRW",
        "HIVE/KRW",
        "HUM/KRW",
        "HUNT/KRW",
        "ICX/KRW",
        "IOST/KRW",
        "IOTA/KRW",
        "IQ/KRW",
        "JST/KRW",
        "KAVA/KRW",
        "KNC/KRW",
        "LINK/KRW",
        "LOOM/KRW",
        "LSK/KRW",
        "LTC/KRW",
        "MANA/KRW",
        "MATIC/KRW",
        "MBL/KRW",
        "MED/KRW",
        "META/KRW",
        "MFT/KRW",
        "MLK/KRW",
        "MOC/KRW",
        "MTL/KRW",
        "MVL/KRW",
        "NEAR/KRW",
        "NEO/KRW",
        "NU/KRW",
        "OMG/KRW",
        "ONG/KRW",
        "ONT/KRW",
        "ORBS/KRW",
        "PLA/KRW",
        "POLY/KRW",
        "POWR/KRW",
        "PUNDIX/KRW",
        "QKC/KRW",
        "QTUM/KRW",
        "REP/KRW",
        "RFR/KRW",
        "SAND/KRW",
        "SBD/KRW",
        "SC/KRW",
        "SNT/KRW",
        "SOL/KRW",
        "SRM/KRW",
        "SSX/KRW",
        "STEEM/KRW",
        "STMX/KRW",
        "STORJ/KRW",
        "STPT/KRW",
        "STRAX/KRW",
        "STRK/KRW",
        "STX/KRW",
        "SXP/KRW",
        "TFUEL/KRW",
        "THETA/KRW",
        "Tokamak Network/KRW",
        "TRX/KRW",
        "TT/KRW",
        "UPP/KRW",
        "VET/KRW",
        "WAVES/KRW",
        "WAXP/KRW",
        "WEMIX/KRW",
        "XEC/KRW",
        "XEM/KRW",
        "XLM/KRW",
        "XRP/KRW",
        "XTZ/KRW",
        "ZIL/KRW",
        "ZRX/KRW",
        "ADA/USDT",
        "BAT/USDT",
        "BCH/USDT",
        "BTC/USDT",
        "DGB/USDT",
        "DOGE/USDT",
        "ETC/USDT",
        "ETH/USDT",
        "LTC/USDT",
        "OMG/USDT",
        "RVN/USDT",
        "SC/USDT",
        "TRX/USDT",
        "TUSD/USDT",
        "XRP/USDT",
        "ZRX/USDT",
    ]
    # ticker_list = [ticker for ticker in ticker_list if '/BTC' in ticker]
    # ticker_list = [ticker for ticker in ticker_list if '/KRW' in ticker]
    ticker_list = [
        ticker for ticker in ticker_list if "/KRW" in ticker or "/BTC" in ticker
    ]

    print("15m")
    for ticker in ticker_list:
        get_target(ticker, "15m")

    print("30m")
    for ticker in ticker_list:
        get_target(ticker, "30m")

    print("1h")
    for ticker in ticker_list:
        get_target(ticker, "1h")

    print("4h")
    for ticker in ticker_list:
        get_target(ticker, "4h")

    print("1d")
    for ticker in ticker_list:
        get_target(ticker, "1d")

    print(datetime.now() - a)
