import ccxt
import time
import datetime
from pprint import pprint
import numpy


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    return (today_money_USDT * 0.03) / price


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


def exit_ALL():
    for i in range(len(is_entering)):
        ticker = list(is_entering.keys())[i]
        sell_amount = is_entering[ticker]
        binance.create_order(ticker, "market", "sell", sell_amount)
    reset = {}
    return reset


def buy_order(ticker):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "buy", buy_amount)
    is_entering[ticker] = float(order["amount"]) * 0.999
    banList.append(ticker)


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    return datetimeobj


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
"""

exchange_class = getattr(ccxt, 'binance')
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = 'FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV'
binance.secret = 'CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87'
binance.load_markets()

"""

ticker_list = [
    "ETH/USDT",
    "NEO/USDT",
    "LTC/USDT",
    "QTUM/USDT",
    "ADA/USDT",
    "XRP/USDT",
    "EOS/USDT",
    "IOTA/USDT",
    "XLM/USDT",
    "ONT/USDT",
    "TRX/USDT",
    "ETC/USDT",
    "ICX/USDT",
    "NULS/USDT",
    "VET/USDT",
    "BCH/USDT",
    "LINK/USDT",
    "WAVES/USDT",
    "BTT/USDT",
    "ONG/USDT",
    "HOT/USDT",
    "ZIL/USDT",
    "ZRX/USDT",
    "FET/USDT",
    "BAT/USDT",
    "XMR/USDT",
    "ZEC/USDT",
    "IOST/USDT",
    "CELR/USDT",
    "DASH/USDT",
    "NANO/USDT",
    "OMG/USDT",
    "THETA/USDT",
    "ENJ/USDT",
    "MITH/USDT",
    "MATIC/USDT",
    "ATOM/USDT",
    "TFUEL/USDT",
    "ONE/USDT",
    "FTM/USDT",
    "ALGO/USDT",
    "GTO/USDT",
    "ERD/USDT",
    "DOGE/USDT",
    "DUSK/USDT",
    "ANKR/USDT",
    "WIN/USDT",
    "COS/USDT",
    "NPXS/USDT",
    "COCOS/USDT",
    "MTL/USDT",
    "TOMO/USDT",
    "PERL/USDT",
    "DENT/USDT",
    "MFT/USDT",
    "KEY/USDT",
    "DOCK/USDT",
    "WAN/USDT",
    "FUN/USDT",
    "CVC/USDT",
    "CHZ/USDT",
    "BAND/USDT",
    "BEAM/USDT",
    "XTZ/USDT",
    "REN/USDT",
    "RVN/USDT",
    "HC/USDT",
    "HBAR/USDT",
    "NKN/USDT",
    "STX/USDT",
    "KAVA/USDT",
    "ARPA/USDT",
    "IOTX/USDT",
    "RLC/USDT",
    "MCO/USDT",
    "CTXC/USDT",
    "TROY/USDT",
    "VITE/USDT",
    "FTT/USDT",
    "OGN/USDT",
    "DREP/USDT",
    "TCT/USDT",
    "WRX/USDT",
    "BTS/USDT",
    "LSK/USDT",
    "BNT/USDT",
    "LTO/USDT",
    "STRAT/USDT",
    "AION/USDT",
    "MBL/USDT",
    "COTI/USDT",
    "STPT/USDT",
    "WTC/USDT",
    "DATA/USDT",
    "XZC/USDT",
    "CTSI/USDT",
    "HIVE/USDT",
    "CHR/USDT",
    "GXS/USDT",
    "ARDR/USDT",
    "LEND/USDT",
    "MDT/USDT",
    "STMX/USDT",
    "KNC/USDT",
    "REP/USDT",
    "LRC/USDT",
    "PNT/USDT",
]

banList = []
is_entering = {}
# today_money_USDT = binance.fetch_balance()['USDT']['total']


# IBS = close - low / high - low


def get_data(day, ticker):
    temp_time = str(
        timestamp_to_datetime(binance.fetch_ohlcv("BTC/USDT", "1d")[-day - 2][0])
    )
    convert = temp_time[:10] + "T" + temp_time[11:19] + "Z"
    timestamp = binance.parse8601(convert)

    ohlcv_1d = binance.fetch_ohlcv(ticker, "1d")[-day - 2]

    ohlcv_5m = binance.fetch_ohlcv(ticker, "5m", timestamp)[180:468]

    # print(ohlcv_1d[0])
    # print(ohlcv_5m[0][0])

    # ohlcv_5m_BTC = binance.fetch_ohlcv('BTC/USDT', '5m', timestamp)[180:468]

    enter_price = ohlcv_5m[15][1]
    exit_price = ohlcv_5m[95][1]
    exit_price2 = ohlcv_5m[97][1]

    # start_BTC = ohlcv_5m_BTC[0][1]
    # end_BTC = ohlcv_5m_BTC[15][1]

    start_BTC = ohlcv_5m[0][1]
    end_BTC = ohlcv_5m[15][1]
    high = ohlcv_1d[2]
    low = ohlcv_1d[3]

    data_1 = (start_BTC - low) / (high - low)
    data_2 = (end_BTC - low) / (high - low)

    if data_1 - data_2 > 0.26:
        temp = (exit_price / enter_price) * 0.99964 * 0.99964 - 1
        result.append(100 * temp)

    if data_2 - data_1 > 0.26:
        temp = (enter_price / exit_price2) * 0.99964 * 0.99964 - 1
        result.append(100 * temp)


tickers = [
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
]
tickers = [
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
]

# 15 - 21 승률 100


def abcd(start, end):
    for i in range(len(tickers)):
        # print(i)
        for j in range(start, end):
            get_data(j, tickers[i])

    plus = []
    minus = []

    for i in range(len(result)):
        if result[i] > 0:
            plus.append(result[i])

    risk_free = 0.038 / 365
    avg = numpy.mean(result)
    std = numpy.std(result)
    size = (avg - risk_free) / (std * std)

    print("최대 수익 거래 :", max(result))
    print("최대 손실 거래 ", min(result))
    print("총 거래 :", len(result))
    print("승률 :", len(plus) / len(result))
    print("평균수익", avg)
    print("포지션 사이징", size)


result = []
abcd(2, 10)


result = []
abcd(11, 20)


result = []
abcd(21, 30)


result = []
abcd(31, 40)


result = []
abcd(41, 50)


result = []
abcd(51, 60)


result = []
abcd(61, 70)


result = []
abcd(71, 80)


result = []
abcd(81, 90)
