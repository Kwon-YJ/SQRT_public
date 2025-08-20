# -*- coding: utf-8 -*-

from pykrx import stock
import parmap
import pandas as pd
from tabulate import tabulate
import Utils
import pandas_ta as ta


import Utils

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


for ticker in ticker_list:
    week_max = binance.fetch_ohlcv(ticker, "1w")
    week_max = [ohlcv[4] for ohlcv in week_max]
    if max(week_max) == week_max[-1]:
        print(ticker)


exit()


def get_position_size(dataframe):
    close = dataframe["종가"].tolist()[-1]
    dataframe.rename(
        columns={"종가": "close", "고가": "high", "저가": "low"}, inplace=True
    )
    atr = dataframe.ta.atr(length=14).tail(1).tolist()[0] * 2
    position_size = f"{round(0.02/(atr/close)*100,2)}%"
    return position_size


def get_result(ticker):
    try:
        name = stock.get_market_ticker_name(ticker)
        if "스팩" in name:
            return "pass"
        df = stock.get_market_ohlcv_by_date("20000101", Today, ticker)
        temp_list = df["종가"].tolist()
        if len(temp_list) < 270:
            return "pass"
        sorted_list = sorted(temp_list)
        if temp_list[-1] == sorted_list[-1] and sorted_list[-2] not in temp_list[-30:]:
            cap = int(
                stock.get_market_cap_by_ticker(Today).loc[ticker, "시가총액"] / 1000000
            )
            size = get_position_size(df)
            return [
                name,
                round(max(temp_list[-250:]) / min(temp_list[-250:]), 1),
                cap,
                size,
            ]
    except:
        print("?", end="")
    return "pass"


def print_result(input_list):
    temp_list = [[], [], [], [], []]

    for idx, item in enumerate(input_list):
        temp_list[0].append(item[0])
        temp_list[1].append(item[1])
        temp_list[2].append(item[2])
        temp_list[3].append(item[3])

    df = pd.DataFrame(
        {
            "name": temp_list[0],
            "max/min": temp_list[1],
            "cap": temp_list[2],
            "size": temp_list[3],
        }
    )
    df["R_gap"] = df["max/min"].rank(method="min")
    df["R_cap"] = df["cap"].rank(method="min", ascending=False)
    df["gap+cap"] = df["R_gap"] + df["R_cap"]

    return tabulate(df, headers="keys", tablefmt="psql")


"""
if __name__ == '__main__':
    global Today
    Today = Utils.get_time()[0]
    # Today = '20210710'

    
    



    konex = stock.get_market_ticker_list(market="KONEX")
    tickers = list(set(stock.get_market_ticker_list(market="ALL")) - set(konex))
    result_ = parmap.map(get_result, tickers , pm_pbar=True, pm_processes=5)

    while(1):
        try:
            result_.remove('pass')
        except:
            break

    print(result_)
    print(print_result(result_))
    Utils.telegram_send(result_)
    Utils.telegram_send(print_result(result_))
"""
