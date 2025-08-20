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


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    # today_money_USDT = float(binance.fetch_balance()['info']['totalWalletBalance']) * coefficient_table[coefficient_value]
    today_money_USDT = 15
    result = today_money_USDT / price
    return binance.amount_to_precision(ticker, amount=result)


def order(ticker):
    # sell_price = get_ohlcv(ticker, '1h', 3)[-2][2]

    temp_ohlcv = get_ohlcv(ticker, "1h", 3)
    sell_price = (temp_ohlcv[-2][2] + temp_ohlcv[-2][4]) / 2

    buy_amount = get_amount(ticker)
    binance.create_order(ticker, "market", "buy", buy_amount)
    binance.create_order(ticker, "limit", "sell", buy_amount, sell_price)


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


def get_tickers():
    base_ticker = list(binance.fetch_tickers().keys())
    base_ticker = [
        base_ticker[i] for i in range(len(base_ticker)) if "/USDT" in base_ticker[i]
    ]
    base_ticker.remove("BTCDOM/USDT")
    return base_ticker


# 매수 종목 선정하기
def get_target(item):
    try:
        ohlcv = get_ohlcv(item, "1h", 400)
        df = pd.DataFrame(
            data=np.array(ohlcv),
            columns=["T", "O", "H", "L", "close", "V", "0", "0", "0", "0", "0", "0"],
        )
        EMA_7 = df.ta.ema(length=7).tolist()[-2]
        EMA_25 = df.ta.ema(length=25).tolist()[-2]
        EMA_99 = df.ta.ema(length=99).tolist()[-2]
        if EMA_7 < EMA_25 and EMA_7 < EMA_99 and EMA_25 < EMA_99:
            ohlcv = ohlcv[-2]
            high_ = ohlcv[2]
            low_ = ohlcv[3]
            if high_ - low_ == 0:
                return None
            close_ = ohlcv[4]
            IBS = (close_ - low_) / (high_ - low_)
            if IBS < 0.1:
                return item
    except Exception as e:
        print(item)
        print(e)
        time.sleep(0.1)
        return None
    return None


binance = ccxt.binance(
    {
        "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "bOHcvOmxqFVGN6FPsJwcnh4QOxw0D6oaFGHjEhpU2pby1bt7EJDb6t9TExauOccU",
        "secret": "Yece0g5APcAZR4sXJl1M007tLL9w9bB7Qp2o3fGFYJjN3f6tfx6lOCq1LdmRk4Ob",
        "enableRateLimit": False,
    }
)
binance.load_markets()


coefficient_table = [
    0.002,
    0.00205,
    0.00210125,
    0.002153781,
    0.002207626,
    0.002262816,
    0.002319387,
    0.002377372,
    0.002436806,
    0.002497726,
    0.002560169,
    0.002624173,
    0.002689778,
    0.002757022,
    0.002825948,
    0.002896596,
    0.002969011,
    0.003043237,
    0.003119317,
    0.0031973,
    0.003277233,
    0.003359164,
    0.003443143,
    0.003529221,
    0.003617452,
    0.003707888,
    0.003800585,
    0.0038956,
    0.00399299,
    0.004092815,
    0.004195135,
    0.004300014,
    0.004407514,
    0.004517702,
    0.004630644,
    0.00474641,
    0.004865071,
    0.004986697,
    0.005111365,
    0.005239149,
    0.005370128,
    0.005504381,
    0.00564199,
    0.00578304,
    0.005927616,
    0.006075807,
    0.006227702,
    0.006383394,
    0.006542979,
    0.006706554,
    0.006874217,
    0.007046073,
    0.007222225,
    0.00740278,
    0.00758785,
    0.007777546,
    0.007971985,
    0.008171284,
    0.008375566,
    0.008584956,
    0.008799579,
    0.009019569,
    0.009245058,
    0.009476185,
    0.009713089,
    0.009955917,
    0.010204814,
    0.010459935,
    0.010721433,
    0.010989469,
    0.011264206,
    0.011545811,
    0.011834456,
    0.012130318,
    0.012433575,
    0.012744415,
    0.013063025,
    0.013389601,
    0.013724341,
    0.014067449,
    0.014419136,
    0.014779614,
    0.015149104,
    0.015527832,
    0.015916028,
    0.016313928,
    0.016721777,
    0.017139821,
    0.017568317,
    0.018007525,
    0.018457713,
    0.018919155,
    0.019392134,
    0.019876938,
    0.020373861,
    0.020883208,
    0.021405288,
    0.02194042,
    0.022488931,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
    0.023051154,
]
ticker_list = get_tickers()
print(ticker_list)
coefficient_value = sum(
    [len(binance.fetch_open_orders(ticker)) for ticker in ticker_list]
)


if __name__ == "__main__":
    while True:
        time.sleep(2)
        time_ = get_time()[1]
        if time_ == "0903":
            ticker_list = get_tickers()
        if time_[2:] == "00":
            time.sleep(5)
            target_list = parmap.map(
                get_target, ticker_list, pm_pbar=False, pm_processes=3
            )
            target_list = list(set(target_list) - set([None]))
            print(target_list)
            for target in target_list:
                try:
                    order(target)
                except:
                    print(f"fail buy {target}")
                    time.sleep(0.5)
                    continue
            time.sleep(59)
            coefficient_value = sum(
                [len(binance.fetch_open_orders(ticker)) for ticker in ticker_list]
            )
