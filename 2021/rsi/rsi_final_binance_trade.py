from collections import UserDict
import multiprocessing
import pandas_ta as ta
import pandas as pd
import numpy as np
import datetime
import urllib
import parmap
import ccxt
import time
import json


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=500):
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={str(limit)}"  # futures
        # url = f'https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={str(limit)}' # spot
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        result = json.loads(text_data)
    except:
        return [[0]]
    result = [list(map(float, result[i])) for i in range(len(result))]
    return result


# get_time()[0] = 오늘 날짜 str
# get_time()[1] = 현재 시각 str
def get_time():
    now = datetime.datetime.now()
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


# 매수 수량 얻기
def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    result = (USDT_size / price) / total_buy_count
    return binance.amount_to_precision(ticker, amount=result)


# 매수 주문 실행
def buy_order(ticker):
    try:
        buy_amount = get_amount(ticker)
        order = binance.create_order(ticker, "market", "buy", buy_amount)
        is_entering[ticker] = float(order["amount"])
    except:
        return None


# 매수 종목 선정하기
def get_target(item):
    try:
        ohlcv_temp = get_ohlcv(item, "15m", 250)
        df = pd.DataFrame(
            data=np.array(ohlcv_temp),
            columns=["0", "0", "close", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
        )  ## rsi(14, high)
        rsi_entry = df.ta.rsi(length=15).tolist()
        if rsi_entry[-2] < 17.5 and item not in list(is_entering.keys()):
            return item
    except Exception as e:
        # except:
        # print(e)
        time.sleep(0.1)
    return None


binance = ccxt.binance(
    {
        "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "f6LEy0POPdaukqwlrnC4KvJbGWkcXRfVmKbsPmFAaPlyL2Rytswf7ilTa3kAjnQh",
        "secret": "sLvrd7ZT6c49yZVlnFRhPvJcIg8z39S6dVwZcIfPhFueA5BAy5UpTT3ZbVZg9zA2",
        # "apiKey":"Wofk7BIStGtvLeCLCIbXVAbxl3KAy03BHafkmGtVqOILF8FZKonaSxqIPCzK4j6i",
        # "secret": "n91lmhQJCOB1ZySmbuTeuefoFlytnnAkjivYazRF1DW4x22v34RN3LXEq5OlHZtR",
        "enableRateLimit": False,
    }
)
binance.load_markets()

is_entering = {}


global total_buy_count
global USDT_size


if __name__ == "__main__":
    ticker_list = [
        "XEM/USDT",
        "NKN/USDT",
        "BAKE/USDT",
        "ZEC/USDT",
        "LRC/USDT",
        "LINA/USDT",
        "YFI/USDT",
        "RVN/USDT",
        "QTUM/USDT",
        "SXP/USDT",
        "REEF/USDT",
        "CVC/USDT",
        "CHZ/USDT",
        "FIL/USDT",
        "MTL/USDT",
        "XRP/USDT",
        "MATIC/USDT",
        "NEO/USDT",
        "COTI/USDT",
        "ALGO/USDT",
        "HBAR/USDT",
        "REN/USDT",
        "BAT/USDT",
        "HOT/USDT",
        "ADA/USDT",
        "AVAX/USDT",
        "AXS/USDT",
        "TRX/USDT",
        "SC/USDT",
        "AKRO/USDT",
        "KNC/USDT",
        "ALPHA/USDT",
        "CHR/USDT",
        "XTZ/USDT",
        "KSM/USDT",
        "DASH/USDT",
        "HNT/USDT",
        "BTS/USDT",
        "ICP/USDT",
        "DOGE/USDT",
        "DGB/USDT",
        "AAVE/USDT",
        "VET/USDT",
        "RLC/USDT",
        "SRM/USDT",
        "ONE/USDT",
        "EGLD/USDT",
        "STORJ/USDT",
        "GTC/USDT",
        "NEAR/USDT",
        "WAVES/USDT",
        "ETH/USDT",
        "1INCH/USDT",
        "EOS/USDT",
        "LUNA/USDT",
        "UNFI/USDT",
        "SUSHI/USDT",
        "OMG/USDT",
        "RSR/USDT",
        "DODO/USDT",
        "CRV/USDT",
        "IOTA/USDT",
        "ICX/USDT",
        "ALICE/USDT",
        "OGN/USDT",
        "BCH/USDT",
        "BLZ/USDT",
        "FTM/USDT",
        "BNB/USDT",
        "SKL/USDT",
        "KAVA/USDT",
        "SOL/USDT",
        "BTC/USDT",
        "OCEAN/USDT",
        "BTCDOM/USDT",
        "SAND/USDT",
        "LINK/USDT",
        "ZRX/USDT",
        "XLM/USDT",
        "MANA/USDT",
        "ANKR/USDT",
        "TRB/USDT",
        "BTT/USDT",
        "THETA/USDT",
        "UNI/USDT",
        "STMX/USDT",
        "KEEP/USDT",
        "IOST/USDT",
        "BAND/USDT",
        "ETC/USDT",
        "ZIL/USDT",
        "ENJ/USDT",
        "LTC/USDT",
        "BZRX/USDT",
        "RUNE/USDT",
        "CTK/USDT",
        "LIT/USDT",
        "ZEN/USDT",
        "ATOM/USDT",
        "SFP/USDT",
        "TOMO/USDT",
        "YFII/USDT",
        "DEFI/USDT",
        "FLM/USDT",
        "BEL/USDT",
        "COMP/USDT",
        "ONT/USDT",
        "1000SHIB/USDT",
        "GRT/USDT",
        "DOT/USDT",
        "TLM/USDT",
        "XMR/USDT",
        "BAL/USDT",
        "MKR/USDT",
        "CELR/USDT",
        "DENT/USDT",
        "SNX/USDT",
    ]

    while True:
        time.sleep(2)
        now = int(get_time()[1][-2:])
        if now % 15 == 0:
            break

    while 1:
        temp = []

        target_list = parmap.map(get_target, ticker_list, pm_pbar=False, pm_processes=4)
        target_list = list(set(target_list) - set([None]))
        total_buy_count = len(target_list)

        USDT_size = float(binance.fetch_balance()["info"]["availableBalance"]) * 0.07

        for target in target_list:
            try:
                balance = binance.fetch_balance()["info"]
                if (
                    float(balance["totalInitialMargin"])
                    / float(balance["totalWalletBalance"])
                    > 0.4
                ):
                    break
                buy_order(target)
            except:
                time.sleep(2)
                continue

        time.sleep(59.5)

        while True:
            time.sleep(1)
            now = int(get_time()[1][-2:])
            if now % 15 == 0:
                break

        for i in range(len(is_entering)):
            try:
                ticker = list(is_entering.keys())[i]
                ohlcv_temp = get_ohlcv(ticker, "15m", 250)
                df = pd.DataFrame(
                    data=np.array(ohlcv_temp),
                    columns=[
                        "0",
                        "0",
                        "0",
                        "close",
                        "0",
                        "0",
                        "0",
                        "0",
                        "0",
                        "0",
                        "0",
                        "0",
                    ],
                )  ## rsi(7, low)
                rsi_exit = df.ta.rsi(length=8).tolist()
                if rsi_exit[-2] > 39:
                    sell_amount = is_entering[ticker]
                    binance.create_order(
                        ticker,
                        "limit",
                        "sell",
                        sell_amount,
                        binance.fetch_order_book(ticker)["bids"][0][0],
                    )
                    temp.append(ticker)
            except:
                time.sleep(5)
                continue

        for i in range(len(temp)):
            del is_entering[temp[i]]
