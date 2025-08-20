import ccxt

# from utils import *
# import Utils
import pickle


from ..Utils.utils import *


# https://m.blog.naver.com/wideeyed/221839634437
# https://blog.doosikbae.com/52
# python -m factory.Data.upbit_data_save

if __name__ == "__main__":

    tickers = [
        "BTC/KRW",
        "ETH/KRW",
        "BCH/KRW",
        "SOL/KRW",
        "AAVE/KRW",
        "LTC/KRW",
        "BSV/KRW",
        "AXS/KRW",
        "BTG/KRW",
        "STRK/KRW",
        "ETC/KRW",
        "DOT/KRW",
        "NEO/KRW",
        "ATOM/KRW",
        "LINK/KRW",
        "WAVES/KRW",
        "REP/KRW",
        "QTUM/KRW",
        "NEAR/KRW",
        "FLOW/KRW",
        "OMG/KRW",
        "GAS/KRW",
        "Tokamak Network/KRW",
        "SAND/KRW",
        "SBD/KRW",
        "XTZ/KRW",
        "THETA/KRW",
        "AQT/KRW",
        "SRM/KRW",
        "KAVA/KRW",
        "EOS/KRW",
        "MANA/KRW",
        "CBK/KRW",
        "LSK/KRW",
        "1INCH/KRW",
        "ENJ/KRW",
        "DAWN/KRW",
        "STX/KRW",
        "MATIC/KRW",
        "MTL/KRW",
        "STORJ/KRW",
        "SXP/KRW",
        "HIVE/KRW",
        "ALGO/KRW",
        "PLA/KRW",
        "STRAX/KRW",
        "MLK/KRW",
        "KNC/KRW",
        "ADA/KRW",
        "ICX/KRW",
        "ARK/KRW",
        "BAT/KRW",
        "IOTA/KRW",
        "PUNDIX/KRW",
        "BORA/KRW",
        "XRP/KRW",
        "ZRX/KRW",
        "HUNT/KRW",
        "ONG/KRW",
        "NU/KRW",
        "ONT/KRW",
        "GRS/KRW",
        "CRO/KRW",
        "POLY/KRW",
        "WAXP/KRW",
        "GLM/KRW",
        "POWR/KRW",
        "STEEM/KRW",
        "ELF/KRW",
        "CVC/KRW",
        "HUM/KRW",
        "CHZ/KRW",
        "HBAR/KRW",
        "XLM/KRW",
        "AERGO/KRW",
        "MOC/KRW",
        "ARDR/KRW",
        "TFUEL/KRW",
        "DOGE/KRW",
        "UPP/KRW",
        "FCT2/KRW",
        "XEM/KRW",
        "DKA/KRW",
        "ANKR/KRW",
        "META/KRW",
        "STPT/KRW",
        "TRX/KRW",
        "ORBS/KRW",
        "VET/KRW",
        "LOOM/KRW",
        "SNT/KRW",
        "ZIL/KRW",
        "SSX/KRW",
        "JST/KRW",
        "MED/KRW",
        "IOST/KRW",
        "STMX/KRW",
        "QKC/KRW",
        "SC/KRW",
        "RFR/KRW",
        "IQ/KRW",
        "AHT/KRW",
        "MVL/KRW",
        "TT/KRW",
        "CRE/KRW",
        "MFT/KRW",
        "MBL/KRW",
        "BTT/KRW",
        "XEC/KRW",
    ]

    All_ohlcv = []

    # for j in range(1, 200):
    for j in range(125, 200):

        print(j, "일 전 부터", j - 1, "일 전 까지")

        day = j
        temp_time = timestamp_to_datetime(
            upbit.fetch_ohlcv("BTC/KRW", "1d")[-day - 1][0] - 32500000
        )[2]

        convert = temp_time[:10] + "T" + temp_time[11:19] + "Z"
        timestamp = upbit.parse8601(convert)

        for i in range(len(tickers)):
            temp = upbit.fetch_ohlcv(tickers[i], "15m", timestamp)
            All_ohlcv.append(temp)

        file_name = f"{j}.pickle"

        with open(file_name, "wb") as fw:
            pickle.dump(All_ohlcv, fw)

        All_ohlcv.clear()
