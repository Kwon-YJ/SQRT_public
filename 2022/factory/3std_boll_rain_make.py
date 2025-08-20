# -*- coding:utf-8 -*-
import enum
import Utils
import numpy as np
import datetime
import time
import random
import pandas_ta as ta
import pandas as pd


def get_bband(
    ohlcv,
) -> list:  # [lower band, ma, upper band, band width, min-max scale percentage]
    # print(len(ohlcv))

    if len((ohlcv[0])) != 6:
        ohlcv = [item[:6] for item in ohlcv]

    data = pd.DataFrame(
        data=np.array(ohlcv), columns=["Time", "Open", "High", "Low", "Close", "V"]
    )  ## rsi(15, high)
    # result = data.ta.bbands(std = 4, length = 20).values.tolist()[-1]

    result = data.ta.bbands(std=3, length=20).values.tolist()[-2]

    return result


def log_maker(ohlcv, ticker_name) -> None:
    is_entering = False
    for i in range(100, len(ohlcv)):
        low = ohlcv[i][3]
        if is_entering == False:
            bband = get_bband(ohlcv[i - 100 : i])
            if bband == None:
                continue
            # relative_position = bband[-1]
            lower_band = bband[0]
            if low < lower_band:
                entry_price = lower_band
                target_price = entry_price * 1.004
                # liquidity_close_price = entry_price * 0.95
                liquidity_close_price = entry_price * 0.1
                is_entering = True
                continue
        else:
            high = ohlcv[i][2]
            if low < liquidity_close_price:
                exit_price = liquidity_close_price
                earning = (exit_price / entry_price * Slippage - 1) * 100
                print(
                    f"{  ticker_name}  buy : {round(entry_price, 8)}  //  sell : {round(exit_price, 8)}   {round(earning, 2)}"
                )
                buy_sell_log.append(earning)
                is_entering = False
                continue
            if high > target_price:
                exit_price = target_price
                earning = (exit_price / entry_price * Slippage - 1) * 100
                print(
                    f"{  ticker_name}  buy : {round(entry_price, 8)}  //  sell : {round(exit_price, 8)}   {round(earning, 2)}"
                )
                buy_sell_log.append(earning)
                is_entering = False
                continue
    if is_entering != False:
        earning = (ohlcv[-1][4] / entry_price * Slippage - 1) * 100
        print(
            f"{  ticker_name}  buy : {round(entry_price, 8)}  //  sell : {round(ohlcv[-1][4], 8)}   {round(earning, 2)}"
        )
        buy_sell_log.append(earning)
        return None


if __name__ == "__main__":
    binance = Utils.use_binance("future")
    All_ohlcv = []
    buy_sell_log = []
    # Slippage = 0.9982 * 0.9982
    Slippage = 1
    performance = Utils.Performance()
    value = 1.925  # 4h, 1d
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

    del_list = []
    temp_time = Utils.timestamp_to_datetime(
        binance.fetch_ohlcv("BTC/USDT", "1d")[-105][0]
    )[
        2
    ]  # 1h 기준 40의 배수
    convert = temp_time[:10] + "T" + temp_time[11:19] + "Z"
    timestamp = binance.parse8601(convert)

    for ticker in ticker_list:
        # ohlcv = binance.fetch_ohlcv(ticker, '2h',None,999)
        # ohlcv = binance.fetch_ohlcv(ticker, '1h',None,999)
        try:
            ohlcv = binance.fetch_ohlcv(ticker, "15m", None, 999)
            # ohlcv = binance.fetch_ohlcv(ticker, '4h',timestamp,999)
        except:
            time.sleep(0.1)
            continue
        if len(ohlcv) == 999:
            All_ohlcv.append(ohlcv)
        else:
            print(len(ohlcv))
            del_list.append(ticker)
    for ticker in del_list:
        ticker_list.remove(ticker)

    """for day in range(997, 0, -1):
        time_stamp_ = All_ohlcv[0][-day][0]
        log_maker(day)
        if buy_sell_log != []:
            date_ = Utils.timestamp_to_datetime(time_stamp_)
            print(f'Trading Date : {date_}')
        performance.calculating(buy_sell_log)
        buy_sell_log.clear()"""

    for i, ohlcv in enumerate(All_ohlcv):
        log_maker(ohlcv, ticker_list[i])

    performance.calculating(buy_sell_log)
    performance.total_calculating()
    print(performance.zero_trade_log)
    print(f"{value} : {int(performance.money_simulation())}")
