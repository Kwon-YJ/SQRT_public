import ccxt
import time
import datetime
from pprint import pprint
from matplotlib import pyplot as plt


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
    # ohlcv_1h = binance.fetch_ohlcv(ticker, '1h', timestamp)[15:39]
    ohlcv_5m = binance.fetch_ohlcv(ticker, "5m", timestamp)[180:468]

    high = ohlcv_1d[2]
    low = ohlcv_1d[3]

    # print(ohlcv_1d[0])
    # print(ohlcv_5m[0][0])

    temp = []

    for i in range(len(ohlcv_5m)):
        data_ = (ohlcv_5m[-i][1] - low) / (high - low)
        # temp.append(data_)
        result[i].append(data_)


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


result = []

for i in range(288):
    result.append([])
temp = []

start_end = [41, 80]

for i in range(start_end[0], start_end[1]):
    get_data(i, "BTC/USDT")

for i in range(len(result)):
    a = sum(result[i]) / len(result[i])
    print(a)
    temp.append(a)

plt.plot(temp)
file_name = "12121" + str(start_end[0]) + "_" + str(start_end[1]) + ".png"

plt.savefig(file_name, dpi=300)
